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

	







if __name__ == '__main__':
	
	with open('./database/secrets.json') as file:
		secrets = json.load(file)
		file.close()

	bit = Bittrex(secrets)

	tickerVal = bit.get_ticker('BTC-RVN')['result']

	bid = tickerVal['Bid']
	ask = tickerVal['Ask']
	last = tickerVal['Last']

	print(format(bid, '.8f'))
	print(format(ask, '.8f'))
	print(format(last, '.8f'))
