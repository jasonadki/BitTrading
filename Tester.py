from Bittrex import Bittrex
from DataGrabber import DataGrabber
import pandas as pd
import json


class Tester():
	"""
	Class that simulates historical backtesting trading.
	Imports data from Data Grabber and will store different
	trading strategies as methods.
	"""

	def __init__(self, histData, startingAmount):
		self.histData = histData
		self.wallet = startingAmount


	def trailingAverage(self, num):
		"""
		Simple Trailing (T) Average Strategy
		When the current value is greater than the T average, sell.
		When the current value is less than the T average, buy

		:param num: <int> The number of data points to use in the T value. Ie, 12 = Trailing 12
		:return: <int> Coins gained... (This should probably be changed to a better value. There will be issues with price flucations of BTC compared to other coin)
		"""

		df = self.histData
		wallet = self.wallet
		holding = False
		coinCount = 0

		# Create moving average column
		df['MA'] = df.iloc[:,1].rolling(window = num).mean()

		# Loop through rows
		for index, row in df.iterrows():
			currentTime = row.iloc[0]
			currentVal = row.iloc[1]
			currentAvg = row.iloc[2]

			# If current price is greater than average and holding SELL
			if currentVal > currentAvg and holding:
				wallet += (currentVal * coinCount * .9975)
				coinCount = 0
				holding = not holding
				print(f'S on {currentTime} ', end = '')

			# If current price is less than average and not holding BUY
			elif currentVal < currentAvg and not holding:
				numCoins = wallet / (currentVal * 1.0025)
				wallet -= (numCoins * currentVal)
				coinCount = numCoins
				holding = not holding
				print(f'B on {currentTime} ', end = '')

			else:
				print(f'N on {currentTime} ', end = '')

			print(format(currentVal, '.8f'), end = '')
			# print(round(currentVal, 8), end = '')
			print(f' Wallet: {round(wallet,8)} coinCount: {round(coinCount,8)}')


		# When done calculate number of coins finished with
		finalVal = wallet + (coinCount * currentVal)


		return finalVal






if __name__ == '__main__':
	
	with open('./database/secrets.json') as file:
		secrets = json.load(file)
		file.close()

	data = DataGrabber(secrets, 'BTC-RVN', 'fiveMin', 'O').get_data()

	data = data.drop(data.index[0])

	newData = Tester(data, .08)

	print(newData.trailingAverage(7))





