from Bittrex import Bittrex
import pandas as pd
import json





class Grapher():
	"""
	Used for handeling all testing functionality
	"""

	def __init__(self, secrets, market, timeInterval):
		self.Bittrex = Bittrex(secrets)
		self.market = market
		self.timeInterval = timeInterval

	def getData(self):
		data = self.Bittrex.get_ticks(self.market, self.timeInterval)

		return data



with open('./database/secrets.json') as file:
	secrets = json.load(file)
	file.close()

test = Tester(secrets, 'BTC-RVN', 'day')

print(test.getData())

# bit = Bittrex('5049a21e38da48389cc641ffa97cf10b', 'c0eb970db3ec48a5b9d99dff6fced2b1')


# df = bit.get_ticks('BTC-RVN', 'day')['result']


# dic = df[0]

# print((dic['T'], dic['O']))
# vals = [(d['T'], d['O']) for d in df]

# print(vals)

# # 2018-08-27T23:51:00