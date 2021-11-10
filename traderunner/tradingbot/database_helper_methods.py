from tradingbot.models import Trade
from API.main import binancey


class HelperMethods:

  def update_database(self):
      x = Trade.objects.all().reverse()

      for trade in x:
        orderid = trade.order_id
        orderdata = binancey.get_order_status(binancey.contracts[f'{trade.symbol}'], trade.orderid) 
        #print(orderid)
        trade.status = orderdata.status
        trade.save()

  def working(self):
    print("This is working")

    x = 5

    return x

