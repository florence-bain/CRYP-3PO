from django.db import models

# Create your models here.

class Trade(models.Model):
  symbol = models.CharField ('Symbol Name', max_length=120)
  trade_date = models.DateTimeField('Trade Date')
  order_id = models.IntegerField('Order ID')
  status = models.CharField('Status', max_length=120)
  bid_price = models.DecimalField('Bid Price', max_digits=12, decimal_places=3)
  ask_price = models.DecimalField('Ask Price', max_digits=12, decimal_places=3)
  side = models.CharField('Side', max_length=120)
  quantity = models.DecimalField('Quantity', max_digits=12, decimal_places=2)
  tif = models.CharField('Time in Force', max_length=120)
  order_price = models.IntegerField('Order Price')
