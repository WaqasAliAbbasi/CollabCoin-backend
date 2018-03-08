from bigchaindb_driver import BigchainDB
from time import sleep
import bigchaindb_driver
import pickle

bdb_root_url = "127.0.0.1:59984"
bdb = BigchainDB(bdb_root_url)
collab_coin = pickle.load(open("collabcoin", "rb"))


def asset_create(order_symbol, purchase_price, order_quantity, player_public_key):
    asset_data = {
        'data': {
            'stock': {
                'symbol': order_symbol,
                'quantity': order_quantity,
                'orderedBy': player_public_key
            },
        },
    }
    metadata = {'price': purchase_price}
    prepared_creation_tx = bdb.transactions.prepare(
          operation='CREATE',
          signers=collab_coin.public_key,
          asset=asset_data,
          metadata=metadata
      )
    fulfilled_creation_tx = bdb.transactions.fulfill(
        prepared_creation_tx, private_keys=collab_coin.private_key)
    bdb.transactions.send(fulfilled_creation_tx)
    tx_id = fulfilled_creation_tx['id']

    trials = 0
    while trials < 60:
        try:
            if bdb.transactions.status(tx_id).get('status') == 'valid':
                print('Tx valid in:', trials, 'secs')
                break
        except bigchaindb_driver.exceptions.NotFoundError:
            trials += 1
            sleep(1)

    if trials == 60:
        print('Tx is still being processed... Bye!')
        exit(0)

    return tx_id


def asset_transfer(tx_id, public_key=collab_coin.public_key, private_key=collab_coin.private_key):
    creation_tx = bdb.transactions.retrieve(tx_id)
    if creation_tx["operation"] == "CREATE":
        asset_id = creation_tx['id']
    else:
        asset_id = creation_tx['asset']['id']
    transfer_asset = {
        'id': asset_id,
        }
    output_index = 0
    output = creation_tx['outputs'][output_index]

    transfer_input = {
        'fulfillment': output['condition']['details'],
        'fulfills': {
            'output_index': output_index,
            'transaction_id': creation_tx['id'],
        },
        'owners_before': output['public_keys'],
    }

    prepared_transfer_tx = bdb.transactions.prepare(
        operation='TRANSFER',
        asset=transfer_asset,
        inputs=transfer_input,
        recipients=public_key,
        )

    fulfilled_transfer_tx = bdb.transactions.fulfill(
        prepared_transfer_tx,
        private_keys=private_key,)

    bdb.transactions.send(fulfilled_transfer_tx)
    print("success")

    tx_id = fulfilled_transfer_tx['id']

    trials = 0
    while trials < 60:
        try:
            if bdb.transactions.status(tx_id).get('status') == 'valid':
                print('Tx valid in:', trials, 'secs')
                break
        except bigchaindb_driver.exceptions.NotFoundError:
            trials += 1
            sleep(1)

    if trials == 60:
        print('Tx is still being processed... Bye!')
        exit(0)

    return tx_id


def update_wallet(public_key, purchase_price, tx_id):
    asset_data = {
        'data': {
            'deal': {
                'playerID': public_key,
                'transactionAmount': purchase_price,
                'assetID': bdb.transactions.retrieve(tx_id)['asset']['id'],
                'txID': tx_id,
                'type': 'deal'
            },
        },
    }
    prepared_creation_tx = bdb.transactions.prepare(
          operation='CREATE',
          signers=collab_coin.public_key,
          asset=asset_data
      )

    fulfilled_creation_tx = bdb.transactions.fulfill(prepared_creation_tx, private_keys=collab_coin.private_key)
    bdb.transactions.send(fulfilled_creation_tx)
    asset_id = fulfilled_creation_tx['id']

    trials = 0
    while trials < 60:
        try:
            if bdb.transactions.status(asset_id).get('status') == 'valid':
                print('Tx valid in:', trials, 'secs')
                break
        except bigchaindb_driver.exceptions.NotFoundError:
            trials += 1
            sleep(1)

    if trials == 60:
        print('Tx is still being processed... Bye!')
        exit(0)

    return True


def get_order_details(tx_id):
    asset_id = bdb.transactions.retrieve(tx_id)['asset']['id']
    asset_details = bdb.transactions.retrieve(asset_id)
    order_symbol = asset_details['asset']['data']['stock']['symbol']
    order_quantity = asset_details['asset']['data']['stock']['quantity']
    purchase_price = asset_details['metadata']['price']
    return order_symbol, order_quantity, purchase_price


def get_all_assets():
    return bdb.assets.get(search="deal")


def get_owned_assets(public_key):
    owned_assets = []
    assets = bdb.assets.get(search=public_key)
    all_assets = {}
    tx_ids = {}
    for asset in assets:
        if "deal" in asset["data"]:
            if asset["data"]["deal"]["assetID"] in all_assets:
                all_assets[asset["data"]["deal"]["assetID"]] += 1 if asset["data"]["deal"]["transactionAmount"] < 0 else -1
            else:
                all_assets[asset["data"]["deal"]["assetID"]] = 1 if asset["data"]["deal"]["transactionAmount"] < 0 else -1
            tx_ids[asset["data"]["deal"]["assetID"]] = asset["data"]["deal"]["txID"]
    for asset in all_assets.items():
        if asset[1] > 0:
            tx_id = tx_ids[asset[0]]
            order_symbol, order_quantity, purchase_price = get_order_details(tx_id)
            owned_assets.append({
                "symbol": order_symbol,
                "quantity": order_quantity,
                "purchasePrice": "$" + str(-1*round(purchase_price,2)),
                "txID": tx_id
            })
    return owned_assets

