from django.http.request import HttpRequest
from django.test import TestCase
from tradingbot.models import Trade
from datetime import datetime, timezone 
from django.urls import resolve
from tradingbot.views import home
from API.strategies import Strategies


# Create your tests here.

# Not testing authentication, feels redundant as authentication is inbuilt with Django..

class MockCandle:
    def __init__(self):
        self.close = 0

# Need to refactor tests for DRY principles

# class MockArray:
#     def __init__(self):
#         self.array = []

#     def iterate_array(self):
#         x = list(range(1, 201))

#         for el in x:
#             candle = MockCandle()
#             candle.close = (x.index(el)) + 1
#             print(candle.close)
#             self.array.append(candle)
    


class Strategy(TestCase):

    def test_goldencross_strategy(self):
        strategy = Strategies()
       
        x = list(range(1, 201))
        arr = []

        for el in x:
            candle = MockCandle()
            candle.close = (x.index(el)) + 1
            print(candle.close)
            arr.append(candle)  

        self.assertEqual(strategy.golden_cross(arr), 175.5)

    def test_sell_strategy_trade(self):

        strategy = Strategies()
       
        x = list(range(1, 201))
        arr = []

        for el in x:
            candle = MockCandle()
            candle.close = (x.index(el)) + 1
            print(candle.close)
            arr.append(candle)  

        self.assertEqual(strategy.sell_strategy(arr, 10), 'Hold')


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve ('/home')
        self.assertEqual(found.func, home)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>Home</title>', html) 
        self.assertTrue(html.endswith('</html>'))



class TestTradeInput(TestCase):
  def setUp(self):
    Trade.objects.create(symbol="BTCUSD", trade_date= datetime.now(),
    order_id = 12345765, status="NEW", bid_price = 200.00, ask_price = 150.000, side ="BUY",
    quantity= 1, tif = "GTC", order_price = 250)

#   def test_symbol_label(self):
#       bitcoin_instance = Trade.objects.get(id=1)
#       field_label = bitcoin_instance._meta.get_field('symbol').verbose_name
#       self.assertEqual(field_label, 'symbol')

  def test_symbol_ticker_is_present(self):
      trade = Trade.objects.get(symbol= 'BTCUSD')
      expect_symbol_ticker = trade.symbol
      self.assertEqual(str(trade.symbol), expect_symbol_ticker)

  def test_quantity_maximum_digits(self):
      trade = Trade.objects.get(symbol= 'BTCUSD')
      max_digits = trade._meta.get_field('quantity').max_digits
      self.assertEqual(max_digits,12)
  
  def test_setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

#   def setUp(self):
#       print("setUp: Run once for every test method to setup clean data.")
#       pass

  def test_false_is_false(self):
      print("Method: test_false_is_false.")
      self.assertFalse(False)

#   def test_false_is_true(self):
#       print("Method: test_false_is_true.")
#       self.assertTrue(False)

  def test_one_plus_one_equals_two(self):
      print("Method: test_one_plus_one_equals_two.")
      self.assertEqual(1 + 1, 2)