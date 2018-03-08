import ita, random
client = ita.Account("waqasabbasi14@gmail.com", "waqas123")

def order(order_action,order_symbol,order_quantity):
    if order_action == "BUY":
        purchase_price = ita.get_quote(order_symbol)
        #client.trade(order_symbol, ita.Action.buy, order_quantity)
        return -(purchase_price*int(order_quantity))
    elif order_action == "SELL":
        purchase_price = ita.get_quote(order_symbol)
        #client.trade(order_symbol, ita.Action.sell, order_quantity)
        return round((purchase_price*round(random.uniform(0.6,1.3),2))*int(order_quantity),2)
    else:
        return False