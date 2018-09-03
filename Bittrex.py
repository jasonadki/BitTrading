import requests
import time
import json
import urllib.parse
import hmac
import hashlib

BUY_ORDERBOOK = 'buy'
SELL_ORDERBOOK = 'sell'
BOTH_ORDERBOOK = 'both'

PUBLIC_SET = ['getmarkets', 'getcurrencies',
				'getticker', 'getmarketsummaries',
				'getorderbook', 'getmarkethistory']

MARKET_SET = ['getopenorders', 'cancel',
				'sellmarket', 'selllimit',
				'buymarket', 'buylimit']

ACCOUNT_SET = ['getbalances', 'getbalance',
				'getdepositaddress', 'withdraw',
				'getorder', 'getorderhistory',
				'getwithdrawalhistory', 'getdeposithistory']



class Bittrex():
	"""
	Used for requesting Bittrex
	"""

	def __init__(self, secrets):
		self.api_key = str(secrets['bittrex']['api_key'])
		self.api_secret = str(secrets['bittrex']['api_secret'])
		self.public_set = set(PUBLIC_SET)
		self.market_set = set(MARKET_SET)
		self.account_set = set(ACCOUNT_SET)

	def api_request(self, method, options = None):
		"""
		Sends request to Bittrex api with the given method and options

		:param method: <str> Api request to be sent
		:param options: <str> Additional options for request
		:return: <dict> JSON response from Bittrex
		"""

		if not options:
			options = {}
		nonce = str(int(time.time() * 1000)) # Not needed at the moment but will be in the future
		base_url = 'https://bittrex.com/api/v1.1/%s/'
		request_url = ''

		#https://bittrex.com/api/v1.1/market/selllimit?apikey=API_KEY&market=BTC-LTC&quantity=1.2&rate=1.3
		#https://bittrex.com/api/v1.1/public/getmarkets
		if method in self.public_set:
			request_url = (base_url % 'public') + method + '?'
		elif method in self.market_set:
			request_url = (base_url % 'market') + method + '?apikey=' + self.api_key + "&nonce=" + nonce + '&'
		elif method in self.account_set:
			request_url = (base_url % 'account') + method + '?apikey=' + self.api_key + "&nonce=" + nonce + '&'
		else: # This is used for the historical data call. Does not follow standard call
			request_url = ('https://bittrex.com/api/v2.0/%s/' % 'pub/market') + method + '?'

		# Add the additional options as url components	
		request_url += urllib.parse.urlencode(options) 

		# Create HMAC-SHA512 signing
		signature = hmac.new(self.api_secret.encode(), request_url.encode(), hashlib.sha512).hexdigest()

		# Create apisign header
		headers = {'apisign': signature}

		# Send request to Bittrex api
		response = requests.get(request_url, headers = headers)

		return response.json()

	def get_markets(self):
		"""
		Used to get the open and available trading markets
		at Bittrex along with other meta data.

		:return: <dict> Available market info in JSON
		"""
		return self.api_request('getmarkets')

	def get_currencies(self):
		"""
		Used to get all supported currencies at Bittrex
		along with other meta data.

		:return: <dict> Supported currencies info in JSON
		"""
		return self.api_request('getcurrencies')

	def get_ticker(self, market):
		"""
		Used to get the current tick values for a market.

		:param market: <str> String literal for the market (ex: BTC-LTC)
		:return: <dict> Current values for given market in JSON
		"""
		return self.api_request('getticker', {'market': market})

	def get_market_summaries(self):
		"""
		Used to get the last 24 hour summary of all active exchanges

		:return: <dict> Summaries of active exchanges in JSON
		"""
		return self.api_request('getmarketsummaries')

	def get_orderbook(self, market, depth_type, depth=20):
		"""
		Used to get retrieve the orderbook for a given market

		:param market: <str> String literal for the market (ex: BTC-LTC)
		:param depth_type: <str> buy, sell or both to identify the type of orderbook to return.
								Use constants BUY_ORDERBOOK, SELL_ORDERBOOK, BOTH_ORDERBOOK
		:param depth: <int> how deep of an order book to retrieve. Max is 100, default is 20
		:return: <dict> Orderbook of market in JSON
		"""
		return self.api_request('getorderbook', {'market': market, 'type': depth_type, 'depth': depth})

	def get_market_history(self, market):
		"""
		Used to retrieve the latest trades that have occured for a
		specific market.

		:param market: <str> String literal for the market (ex: BTC-LTC)
		:return: <dict> Market history in JSON
		"""
		return self.api_request('getmarkethistory', {'market': market})

	def buy_limit(self, market, quantity, rate):
		"""
		Used to place a buy order in a specific market. Use buylimit to place
		limit orders Make sure you have the proper permissions set on your
		API keys for this call to work

		:param market: <str> String literal for the market (ex: BTC-LTC)
		:param quantity: <float> The amount to purchase
		:param rate: <float> The rate at which to place the order.
			This is not needed for market orders
		:return: <dict> 
		"""
		return self.api_request('buylimit', {'market': market, 'quantity': quantity, 'rate': rate})

	def sell_limit(self, market, quantity, rate):
		"""
		Used to place a sell order in a specific market. Use selllimit to place
		limit orders Make sure you have the proper permissions set on your
		API keys for this call to work

		:param market: <str> String literal for the market (ex: BTC-LTC)
		:param quantity: <float> The amount to purchase
		:param rate: <float> The rate at which to place the order.
			This is not needed for market orders
		:return: <dict> 
		"""
		return self.api_request('selllimit', {'market': market, 'quantity': quantity, 'rate': rate})

	def cancel(self, uuid):
		"""
		Used to cancel a buy or sell order

		:param uuid: <str> uuid of buy or sell order
		:return: <dict> 
		"""
		return self.api_request('cancel', {'uuid': uuid})

	def get_open_orders(self, market):
		"""
		Get all orders that you currently have opened. A specific market can be requested

		:param market: <str> String literal for the market (ie. BTC-LTC)
		:return: <dict> Open orders info in JSON
		"""
		return self.api_request('getopenorders', {'market': market})

	def get_balances(self):
		"""
		Used to retrieve all balances from your account

		:return: <dict> Balances info in JSON
		"""
		return self.api_request('getbalances', {})

	def get_balance(self, currency):
		"""
		Used to retrieve the balance from your account for a specific currency

		:param currency: <float> String literal for the currency (ex: LTC)
		:return: <dict> Balance info in JSON
		"""
		return self.api_request('getbalance', {'currency': currency})

	def get_deposit_address(self, currency):
		"""
		Used to generate or retrieve an address for a specific currency

		:param currency: <str> String literal for the currency (ie. BTC)
		:return: <dict> Address info in JSON
		"""
		return self.api_request('getdepositaddress', {'currency': currency})

	def withdraw(self, currency, quantity, address):
		"""
		Used to withdraw funds from your account

		:param currency: <str> String literal for the currency (ie. BTC)
		:param quantity: <float> The quantity of coins to withdraw
		:param address: <str> The address where to send the funds.
		:return: <dict> 
		"""
		return self.api_request('withdraw', {'currency': currency, 'quantity': quantity, 'address': address})

	def get_order(self, uuid):
		"""
		Used to get an order from your account

		:param uuid: <str> The order UUID to look for
		:return: <dict> 
		"""
		return self.api_request('getorder', {'uuid': uuid})

	def get_order_history(self, market = ""):
		"""
		Used to retrieve your order history

		:param market: <str> Bittrex market identifier (i.e BTC-DOGE)
		:return: <dict> 
		"""
		return self.api_request('getorderhistory', {"market": market})
	
	def get_withdrawal_history(self, currency = ""):
		"""
		Used to retrieve your withdrawal history

		:param currency: <str> String literal for the currency (ie. BTC) (defaults to all)
		:return: <dict> 
		"""
		return self.api_request('getwithdrawalhistory', {"currency": currency})

	def get_deposit_history(self, currency = ""):
		"""
		Used to retrieve your deposit history

		:param currency: <str> String literal for the currency (ie. BTC) (defaults to all)
		:return: <dict> 
		"""
		return self.api_request('getdeposithistory', {"currency": currency})

	def get_ticks(self, market = "", tickInterval = ""):
		"""
		Used to get historical data for market.

		:param market: <str> String literal for the market (ex: BTC-LTC)
		:param tickInterval: <str> String literal time delta (ex: oneMin, fiveMin, thirtyMin, day, )
		:return: <dict> Historical data in JSON
		"""

		return self.api_request('GetTicks', {'marketName': market, 'tickInterval': tickInterval})