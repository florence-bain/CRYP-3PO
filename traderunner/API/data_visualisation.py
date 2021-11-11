import datetime
from API.main import binancey

candlesticks_btc  = binancey.get_historical_candles(binancey.contracts['BTCBUSD'], '1d')
candlesticks_mon  = binancey.get_historical_candles(binancey.contracts['XMRUSDT'], '1d')
candlesticks_lite  = binancey.get_historical_candles(binancey.contracts['LTCUSDT'], '1d')
 
filtered_btc = candlesticks_btc[-30:]
filtered_mon = candlesticks_mon[-30:]
filtered_lite = candlesticks_lite[-30:]

x_values = []

btc_high = []
btc_close = []

mon_high = []
mon_close = []

lite_high = []
lite_close = []

for figure in filtered_btc:
    btc_high.append(figure.high)
    btc_close.append(figure.close)
    time = datetime.datetime.fromtimestamp((figure.timestamp)/1000)
    x_values.append(time.strftime("%m/%d/%Y"))
    
for figure in filtered_mon:
    mon_high.append(figure.high)
    mon_close.append(figure.close)

for figure in filtered_lite:
    lite_high.append(figure.high)
    lite_close.append(figure.close)
