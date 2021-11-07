import tkinter as tk
import logging

from connectors.binance_futures import BinanceFuturesClient

logger = logging.getLogger()

logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

if __name__ == '__main__':

    binance = BinanceFuturesClient("ecf3e2fd84f4526cc38205048922901628a5cc50a95f5be5794666a7bdf8c90b",
                                   "b1c0a1eaaa5deab418db2572c6e4e41334bd8d2150a513675dcb119db34c338f", True)

    print(binance.contracts)
    #print(binance.place_order(binance.contracts['BTCUSDT'], "BUY", 0.05, "LIMIT", 2000, "GTC"))

    root = tk.Tk()
    root.mainloop()
