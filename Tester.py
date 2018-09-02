from Bittrex import Bittrex
from DataGrabber import DataGrabber
import pandas as pd
import json






if __name__ == '__main__':
	
	with open('./database/secrets.json') as file:
		secrets = json.load(file)
		file.close()

	data = DataGrabber(secrets, 'BTC-RVN', 'day', 'O').get_data()

	data = data.drop(data.index[0])

	
	