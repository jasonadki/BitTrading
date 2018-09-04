from Bittrex import Bittrex
from DataGrabber import DataGrabber
import pandas as pd
import json
import time

class Trader():
	"""
	Used for actual live trading.
	Should resemble the Tester class with exception to more calls to Bittrex.
	All methods used in here need to be backtested with the Tester Class.
	"""

	def __init__(self, secrets, market):
		self.Bittrex = Bittrex(secrets)
		self.market = market

	def get_current_bid(self):
		"""
		Get the current Bid Price for the given market.
		Bid: Maximum price that a buyer is willing to pay

		:return: <float> Largest Bid Value
		"""

		return self.Bittrex.get_ticker(self.market)['result']['Bid']

	def get_current_ask(self):
		"""
		Get the current Ask Price for the given market.
		Ask: Minimum price that a seller is willing to pay

		:return: <float> Smallest Ask Value
		"""

		return self.Bittrex.get_ticker(self.market)['result']['Ask']

	def get_last_trade(self):
		"""
		Get the last transaction price for the given market.
		Can be either a Sell or a Purchase

		:return: <float> Last Transaction Price
		"""

		return self.Bittrex.get_ticker(self.market)['result']['Last']

	def get_order_book(self, book_type = None):
		"""
		Get order book for current Bids for the given market.

		:param book_type: <str> Which types of orders to return
		:return: <DataFrame> DataFrame of current bids
		"""

		buy_book = self.Bittrex.get_orderbook(self.market, 'buy')['result']
		buy_book = pd.DataFrame(buy_book)
		buy_book['type'] = 'buy'

		sell_book = self.Bittrex.get_orderbook(self.market, 'sell')['result']
		sell_book = pd.DataFrame(sell_book)
		sell_book['type'] = 'sell'

		order_book = buy_book.append(sell_book, ignore_index = True)

		# Check to see if a specific book is requested
		if book_type is None:
			return order_book
		else:
			return order_book.loc[order_book['type'] == book_type].reset_index(drop = True)

	def place_buy(self, quantity, price):
		"""
		Place a purchace order for the given market.

		:param quantity: <float> The amount to purchase
		:param price: <float> The rate at which to place the order
		:return: <dict> Confirmation
		"""

		return self.Bittrex.buy_limit(self.market, quantity, price)

	def place_sell(self, quantity, price):
		"""
		Place a sell order for the given market.

		:param quantity: <float> The amount to sell
		:param price: <float> The rate at which to place the order
		:return: <dict> Confirmation
		"""

		return self.Bittrex.sell_limit(self.market, quantity, price)

	def get_balances(self):
		"""
		Get list of available balances for all coins you own

		:return: <dict> Available balances
		"""

		df = bit.get_balances()['result']

		coin = [k['Currency'] for k in df]
		amount = [k['Available'] for k in df]

		result  = dict(zip(coin, amount))

		return result