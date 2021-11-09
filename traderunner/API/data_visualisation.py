import datetime
from re import X
import pandas as pd
import numpy as np
import plotly.express as px 
from API.main import binancey
import os


candlesticks  = binancey.get_historical_candles(binancey.contracts['BTCBUSD'], '1d')

filtered_btc = candlesticks[-30:]
filtered_eth = candlesticks

x_values = []
y_values = []

for figure in filtered_btc:
    y_values.append(figure.high)
    x_values.append(str(datetime.datetime.fromtimestamp((figure.timestamp)/1000).date))

      
x_axis = x_values
y_axis = y_values

# df = pd.DataFrame(dict(
#   y = x_values,
#   x = y_values

# ))

# df = df.sort_values(by="x")
# fig = px.line(df, x="x", y="y", title="Sorted Input") 
# fig.show()

# # plot.write_html(outpath,
# #                 full_html=False,
# #                 include_plotlyjs='cdn')











# #from binance import Client
# import pprint, os

# import sys
# import binance
# print(sys.path)
# print("this system check has passed")

# pprint.pprint(os.path.abspath(binance.__file__))



# #from API.connectors.binance_futures import BinanceFuturesClient
# #from traderunner.API.main import binance


# #binance = BinanceFuturesClient("ecf3e2fd84f4526cc38205048922901628a5cc50a95f5be5794666a7bdf8c90b",
#                                   # "b1c0a1eaaa5deab418db2572c6e4e41334bd8d2150a513675dcb119db34c338f", True)

# symbol = 'BTCUSDT'
# # change for USD 


# start_time = "1 March, 2021"
# end_time =  "1 April, 2021"


# #binance.get_historical_candles(binance.contracts['BTCBUSD'], '1d')

# # get historical data from binance API
# #klines = np.array(binance.get_historical_candles(binance.contracts[f"{symbol}"], '1h'))

# # reshape date to pandas
# #df = pd.DataFrame(klines.reshape(-1, 1000), dtype=float, columns=('Open Time','Open','High','Low','Close','Volume','Close time','Quote asset volume','Number of trades','Taker buy base asset volume','Taker buy quote asset volume','Ignore'))
# #df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')

# # plot candlesticks using plotly
# # fig = go.Figure(data=[go.Candlestick(x=df['Open Time'],
# #                 open=df['Open'],
# #                 high=df['High'],
# #                 low=df['Low'],
# #                 close=df['Close'])])
# # #fig.show()

# #fig.write_html("../../tradingbot/templates")