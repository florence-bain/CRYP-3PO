import datetime
from API.main import binancey

candlesticks_btc  = binancey.get_historical_candles(binancey.contracts['BTCBUSD'], '1d')
candlesticks_eth  = binancey.get_historical_candles(binancey.contracts['ETHUSDT'], '1d')
candlesticks_doge  = binancey.get_historical_candles(binancey.contracts['DOGEUSDT'], '1d')
 
filtered_btc = candlesticks_btc[-30:]
filtered_eth = candlesticks_eth[-30:]
filtered_doge = candlesticks_doge[-30:]

x_values = []

btc_high = []
btc_close = []

eth_high = []
eth_close = []

doge_high = []
doge_close = []

for figure in filtered_btc:
    btc_high.append(figure.high)
    btc_close.append(figure.close)
    time = datetime.datetime.fromtimestamp((figure.timestamp)/1000)
    x_values.append(time.strftime("%m/%d/%Y"))
    
for figure in filtered_eth:
    eth_high.append(figure.high)
    eth_close.append(figure.close)

for figure in filtered_doge:
    doge_high.append(figure.high)
    doge_close.append(figure.close)
