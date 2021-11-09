import logging
import requests
import time
import typing

from datetime import datetime, timezone
import pytz

from urllib.parse import urlencode

import hmac
import hashlib

import websocket
import json

import threading

from tradingbot.models import Trade

from API.strategies import Strategies

from API.models import * 

logger = logging.getLogger()

# valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M


class BinanceFuturesClient:
    def __init__(self, public_key: str, secret_key: str, testnet: bool):
        if testnet:
            self._base_url = "https://testnet.binancefuture.com"
            self._wss_url = "wss://stream.binancefuture.com/ws"
        else:
            self._base_url = "https://fapi.binance.com"
            self._wss_url = "wss://fstream.binance.com/ws"

        self._public_key = public_key
        self._secret_key = secret_key

        self._headers = {'X-MBX-APIKEY': self._public_key}

        self.contracts = self.get_contracts()
        self.balances = self.get_balances()

        self.prices = dict()

        self._ws_id = 1
        self._ws = None

        self.strategy_price_btc = ""
        self.strategy_price_eth = ""
        self.strategy_price_ltc = ""

        t = threading.Thread(target=self._start_ws)
        t.start()

        logger.info('Binance Futures Client Successfully Initialized')

    def _generate_signature(self, data: typing.Dict) -> str:
        return hmac.new(self._secret_key.encode(), urlencode(data).encode(), hashlib.sha256).hexdigest()

    def _make_request(self, method: str, endpoint: str, data: typing.Dict):
        if method == "GET":
            try:
                response = requests.get(self._base_url + endpoint, params=data, headers=self._headers)
            except Exception as e:
                logger.error("Connection error while making %s request to %s: %s", method, endpoint, e)
                return None

        elif method == "POST":
            try:
                response = requests.post(self._base_url + endpoint, params=data, headers=self._headers)
            except Exception as e:
                logger.error("Connection error while making %s request to %s: %s", method, endpoint, e)
                return None

        elif method == "DELETE":
            try:
                response = requests.delete(self._base_url + endpoint, params=data, headers=self._headers)
            except Exception as e:
                logger.error("Connection error while making %s request to %s: %s", method, endpoint, e)
                return None

        else:
            raise ValueError()

        if response.status_code == 200:
            return response.json()
        else:
            logger.error("Error while making %s request to %s: %s (error code %s",
                         method, endpoint, response.json(), response.status_code)
            return None

    def get_contracts(self) -> typing.Dict[str, Contract]:
        exchange_info = self._make_request("GET", "/fapi/v1/exchangeInfo", dict())

        contracts = dict()

        if exchange_info is not None:
            for contract_data in exchange_info['symbols']:
                contracts[contract_data['pair']] = Contract(contract_data)

        return contracts

    def get_historical_candles(self, contract: Contract, interval: str) -> typing.List[Candle]:
        data = dict()
        data['symbol'] = contract.symbol
        data['interval'] = interval
        data['limit'] = 1000

        raw_candles = self._make_request("GET", "/fapi/v1/klines", data)

        candles = []

        if raw_candles is not None:
            for c in raw_candles:
                candles.append(Candle(c))

        return candles

    def get_bid_ask(self, contract: Contract) -> typing.Dict[str, float]:
        data = dict()
        data['symbol'] = contract.symbol
        ob_data = self._make_request("GET", "/fapi/v1/ticker/bookTicker", data)

        if ob_data is not None:
            if contract.symbol not in self.prices:
                self.prices[contract.symbol] = {'bid': float(ob_data['bidPrice']), 'ask': float(ob_data['askPrice'])}
            else:
                self.prices[contract.symbol]['bid'] = float(ob_data['bidPrice'])
                self.prices[contract.symbol]['ask'] = float(ob_data['askPrice'])

            return self.prices[contract.symbol]

    def get_balances(self) -> typing.Dict[str, Balance]:
        data = dict()
        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self._generate_signature(data)

        balances = dict()

        account_data = self._make_request("GET", "/fapi/v1/account", data)

        if account_data is not None:
            for a in account_data['assets']:
                balances[a['asset']] = Balance(a)

        return balances

    def place_order(self, contract: Contract, side: str, quantity: float, order_type: str, price=None, tif=None) \
            -> OrderStatus:
        data = dict()
        data['symbol'] = contract.symbol
        data['side'] = side
        data['quantity'] = quantity
        data['type'] = order_type

        if price is not None:
            data['price'] = price

        if tif is not None:
            data['timeInForce'] = tif

        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self._generate_signature(data)

        order_status = self._make_request("POST", "/fapi/v1/order", data)

        if order_status is not None:
            order_status = OrderStatus(order_status)

        return order_status

    def cancel_order(self, contract: Contract, order_id: int) -> OrderStatus:

        data = dict()
        data['orderId'] = order_id
        data['symbol'] = contract.symbol

        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self._generate_signature(data)

        order_status = self._make_request("DELETE", "/fapi/v1/account", data)

        if order_status is not None:
            order_status = OrderStatus(order_status)

        return order_status

    def get_order_status(self, contract: Contract, order_id: int) -> OrderStatus:

        data = dict()
        data['timestamp'] = int(time.time() * 1000)
        data['symbol'] = contract.symbol
        data['order_id'] = order_id
        data['signature'] = self._generate_signature(data)

        order_status = self._make_request("GET", "/fapi/v1/order", data)

        if order_status is not None:
            order_status = OrderStatus(order_status)

        return order_status

    def _start_ws(self):
        self._ws = websocket.WebSocketApp(self._wss_url, on_open=self._on_open, on_close=self._on_close,
                                         on_error=self._on_error, on_message=self._on_message)
        while True:
            try:
                self._ws.run_forever()
            except Exception as e:
                logger.error("Binance error in run_forever() method: %s", e)
            time.sleep(2)

    def _on_open(self, ws):
        logger.info("Binance connection opened")

        strategies = Strategies()
        hist_contracts_btc = self.get_historical_candles(self.contracts['BTCBUSD'], '1d')
        hist_contracts_ltc = self.get_historical_candles(self.contracts['LTCUSDT'], '1d')
        hist_contracts_eth = self.get_historical_candles(self.contracts['ETHUSDT'], '1d')
        
        self.strategy_price_btc = strategies.golden_cross(hist_contracts_btc)
        self.strategy_price_eth = strategies.golden_cross(hist_contracts_eth)
        self.strategy_price_ltc = strategies.golden_cross(hist_contracts_ltc)


        self.subscribe_channel(list(self.contracts.values()), "bookTicker")

    def _on_close(self, ws):
        logger.warning("Binance websocket connection closed")

    def _on_error(self, ws, msg: str):
        logger.error("Binance connections error: %s", msg)

    def _on_message(self, ws, msg: str):

        data = json.loads(msg)

        #print(data)
        #print(self.prices)

        if "e" in data:
            if data['e'] == "bookTicker":

                symbol = data['s']

                if symbol not in self.prices:
                    self.prices[symbol] = {'bid': float(data['b']), 'ask': float(data['a'])}
                else:
                    self.prices[symbol]['bid'] = float(data['b'])
                    self.prices[symbol]['ask'] = float(data['a'])
                    #print(f"This is the litecoin price {self.prices['LTCUSDT']['ask']} and the strategy price {self.strategy_price_ltc}")
                    if symbol == 'BTCBUSD' and self.strategy_price_btc != 'false' and \
                            self.prices[symbol]['bid'] > self.strategy_price_btc:    
                        print("This bitcoin method is working as intended")
                        self.execute_trade(symbol, self.prices[symbol]['bid'], self.prices[symbol]['ask'])
                    elif symbol == 'ETHUSDT_211231' and self.strategy_price_eth != 'false' and \
                             self.prices[symbol]['bid'] > self.strategy_price_eth:    
                             print("This ethereum method is working as intended")
                             self.execute_trade(symbol, self.prices[symbol]['bid'], self.prices[symbol]['ask'])
                    elif symbol == 'LTCUSDT' and self.strategy_price_ltc != 'false' and \
                             self.prices[symbol]['bid'] > self.strategy_price_ltc:    
                             print("This litecoin method is working as intended")
                             self.execute_trade(symbol, self.prices[symbol]['bid'], self.prices[symbol]['ask'])
                    else:
                        pass


    def subscribe_channel(self, contracts: typing.List[Contract], channel: str):
        data = dict()
        data['method'] = "SUBSCRIBE"
        data['params'] = []

        for contract in contracts:
            data['params'].append(contract.symbol.lower() + "@" + channel)
        data['id'] = self._ws_id

        try:
            self._ws.send(json.dumps(data))
        except Exception as e:
            logger.error("Websocket error while subscribing to %s %s updates: %s", len(contracts), channel, e)

        self._ws_id += 1

    def execute_trade(self, symbol_ticker, sym_bid_price, sym_ask_price):

        order_quantity = 0.05
        buy_price = 2000 
        
        x = Trade.objects.latest('trade_date').trade_date

        y = (datetime.now(timezone.utc))
        #print(f"This is the trade date {x}")

        difference = y - x 

        if difference.days > 1:
            print("Now is time to do a trade")
            #need to amend for ticker specific trades
            x = self.place_order(self.contracts['ETHUSDT'], "BUY", order_quantity, "LIMIT", buy_price, "GTC")

            print(f"This is the {x.order_id} and this is the order status {x.status} and the average price {x.status}")
            
            new_trade = Trade(
                symbol = f"{symbol_ticker}",
                trade_date = f"{datetime.now()}",
                order_id = x.order_id,
                status = f"{x.status}",
                bid_price = sym_bid_price,
                ask_price = sym_ask_price,
                side = "BUY",
                quantity = order_quantity,
                tif = "GTC",
                order_price = buy_price,
            )
            new_trade.save()
            logger.info("Bingo, now is a good time to execute a trade")
        else:
            #print("You've already traded enough today")
            pass



      
    

