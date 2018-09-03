from Bittrex import Bittrex
import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt
import csv






class DataGrabber():
	"""
	Used to grab historical data. Making a unqiue class to hold these because
	it will be used in a graphing, testing and live trading applications
	"""

	def __init__(self, secrets, market, timeInterval, priceType):
		self.Bittrex = Bittrex(secrets)
		self.market = market
		self.timeInterval = timeInterval
		self.priceType = priceType
		self.data = pd.DataFrame()


	def clean_historical_data(self, brokenDate):
		"""
		The Bittrex historical data gives time values as '2018-08-27T23:51:00'.
		This function will clean this into a datetime variable.

		:param brokenDate: <str> The messy date from Bittrex
		:return: <datetime> New clean datetime value
		"""

		return datetime.strptime(brokenDate, '%Y-%m-%dT%H:%M:%S')



	def get_data(self):
		"""
		Grab the historical data from Bittrex for the given market
		and return as a Pandas DataFrame.
		(Because who doesn't like Pandas??)
		
		:return: <DataFrame> Two column dataframe of time and price.
		"""

		# Create naming dictionary
		nameDic = {'O':'Open', 'H':'High', 'L':'Low', 'C':'Close', 'V':'Volume', 'T':'Time', 'BV':'BookValue'}

		# Get Bittrex historical data
		data = self.Bittrex.get_ticks(self.market, self.timeInterval)['result']

		# Create dataframe only take the time and chosen variable
		df = pd.DataFrame(data)[['T', self.priceType]]

		# Map column names to appropraite column values
		df.columns = list(map(nameDic.get, list(df)))

		# Fix the time variable that Bittrex gives
		df['Time'] = df['Time'].apply(self.clean_historical_data)

		self.data = df

		return df