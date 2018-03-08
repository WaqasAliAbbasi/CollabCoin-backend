from flask import Flask, request, Response
import json

from investopedia import order
from blockchain import asset_create, asset_transfer, update_wallet, get_order_details, get_owned_assets

app = Flask(__name__, static_url_path='')

@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/asset/order", methods=['POST'])
def asset_order():
    if request.headers['Content-Type'] == 'application/json':
        order_data = request.get_json()
        if all(k in order_data for k in ("playerID", "orderAction")):
            if order_data["orderAction"] == "BUY":
                if all(k in order_data for k in ("orderSymbol", "orderSymbol")):
                    player_public_key = order_data["playerID"]
                    order_action = order_data["orderAction"]
                    order_symbol = order_data["orderSymbol"]
                    order_quantity = order_data["orderQuantity"]

                    purchase_price = order(order_action, order_symbol, order_quantity)
                    if purchase_price < 0:
                        asset_id = asset_create(order_symbol, purchase_price, order_quantity, player_public_key)
                        tx_id = asset_transfer(asset_id, public_key=player_public_key)
                        update_wallet(player_public_key, purchase_price, tx_id)
                        return Response(json.dumps({
                            "status": "success",
                            "txID": tx_id,
                            "playerID": player_public_key,
                            "purchasePrice": -1*purchase_price
                        }))
                    else:
                        return Response(json.dumps({
                            "status": "failure"
                        }))
            elif order_data["orderAction"] == "SELL":
                if all(k in order_data for k in ("privateKey", "txID")):
                    player_public_key = order_data["playerID"]
                    order_action = order_data["orderAction"]
                    player_private_key = order_data["privateKey"]
                    tx_id = order_data["txID"]

                    order_symbol, order_quantity, _ = get_order_details(tx_id)

                    tx_id = asset_transfer(tx_id, private_key=player_private_key)
                    purchase_price = order(order_action, order_symbol, order_quantity)
                    if purchase_price > 0:
                        update_wallet(player_public_key, purchase_price, tx_id)
                        return Response(json.dumps({
                            "status": "success",
                            "txID": tx_id,
                            "playerID": player_public_key,
                            "purchasePrice" : purchase_price
                        }))
                    else:
                        return Response(json.dumps({
                            "status": "failure"
                        }))
                else:
                    return Response(json.dumps({
                        "status": "failure"
                    }))
            else:
                return Response(json.dumps({
                    "status": "failure"
                }))

        else:
            return Response(json.dumps({
                    "status": "failure"
                }))

@app.route("/assets/<public_key>",methods=['GET'])
def assets_list(public_key):
    return Response(json.dumps(get_owned_assets(public_key)))


if __name__ == '__main__':
    app.run()
