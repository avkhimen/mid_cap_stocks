import requests
import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import numpy as np

class Company:
	def __init__(self, ticker):
		self.ticker = ticker

	# def get_market_cap(self):
	# 	try:
	# 		url = 'https://financialmodelingprep.com/api/v3/profile/' + str(self.symbol) + '?apikey=330d2c5a870ebbea33644948eeeaadf0'
	# 		r = requests.get(url)
	# 		rjs = json.loads(r.text)
	# 	except Exception as e:
	# 		print(e)
	# 	else:
	# 		market_cap = float(rjs[0]['mktCap'])
	# 	return market_cap

	# def get_1_year_target(self):

	# 	url = 'https://ca.finance.yahoo.com/quote/' + str(self.symbol)
	# 	xpath = '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div[2]/table/tbody/tr[8]/td[2]/span'

	# 	options = Options()
	# 	options.headless = True
	# 	driver = webdriver.Firefox(options=options)

	# 	try:
	# 		driver.get(url)
	# 		time.sleep(2)
	# 	except Exception as e:
	# 		print(e)
	# 		try:
	# 			driver.get(url)
	# 			time.sleep(2)
	# 		except Exception as e:
	# 			print(e)
	# 			one_year_target = None
	# 	else:
	# 		one_year_target = float(driver.find_element_by_xpath(xpath).get_attribute('innerHTML'))
	# 	finally:
	# 		driver.quit()

	# 	return one_year_target

	def get_1yr_target_and_market_cap(self):

		url = 'https://ca.finance.yahoo.com/quote/' + str(self.ticker)
		target_xpath = '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div[2]/table/tbody/tr[8]/td[2]/span'
		cap_xpath = '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div[2]/table/tbody/tr[1]/td[2]/span'

		options = Options()
		options.headless = True
		driver = webdriver.Firefox(options=options)

		try:
			driver.get(url)
			time.sleep(0.5)
		except Exception as e:
			print(e)
			try:
				driver.get(url)
				time.sleep(0.5)
			except Exception as e:
				print(e)
				one_year_target = None
		else:
			one_year_target = float(driver.find_element_by_xpath(target_xpath).get_attribute('innerHTML'))
			market_cap = str(driver.find_element_by_xpath(cap_xpath).get_attribute('innerHTML'))
			market_cap = self.process_market_cap(market_cap)
		finally:
			driver.quit()

		return market_cap, one_year_target

	@staticmethod
	def process_market_cap(market_cap):
		#Extract last digit from market cap
		last_digit = str(market_cap[-1:])
		first_digits = float(market_cap[:-1])
		if last_digit == 'T':
			multiplier = 1000000000000
		elif last_digit == 'B':
			multiplier = 1000000000
		elif last_digit == 'M':
			multiplier = 1000000
		else:
			multiplier = 1
		#Get market cap
		market_cap = first_digits * multiplier

		return market_cap

	def get_january_price_and_latest_price(self):
		url = ('https://query1.finance.yahoo.com/v7/finance/download/' 
			+ str(self.ticker) 
			+ '?period1=-1325635200&period2=1593302400&interval=1d&events=history')
		df = pd.read_csv(url)
		df = df.set_index(df['Date'])

		jan_price = df.loc['2020-01-02']['Close']
		latest_price = df.iloc[-1]['Close']

		return latest_price, jan_price

	# def get_latest_price(self):
	# 	try:
	# 		url = 'https://financialmodelingprep.com/api/v3/quote/' + str(self.symbol) + '?apikey=330d2c5a870ebbea33644948eeeaadf0'
	# 		r = requests.get(url)
	# 		rjs = json.loads(r.text)
	# 	except Exception as e:
	# 		print(e)
	# 	else:
	# 		price = float(rjs[0]['price'])
	# 	return price

	# def get_january_price(self):
	# 	try:
	# 		url = 'https://financialmodelingprep.com/api/v3/historical-price-full/' + str(self.symbol) + '?serietype=line' + '&apikey=330d2c5a870ebbea33644948eeeaadf0'
	# 		r = requests.get(url)
	# 		day_closing_price_list = json.loads(r.text)['historical']
	# 	except Exception as e:
	# 		print(e)
	# 	else:
	# 		first_day = datetime.strptime(day_closing_price_list[-1]['date'], "%Y-%m-%d")
	# 		jan_2 = datetime.strptime("2020-01-02", "%Y-%m-%d")

	# 		if first_day <= jan_2:
	# 			for item in day_closing_price_list:
	# 				if item['date'] == "2020-01-02":
	# 					jan_price = float(item['close'])
	# 					return jan_price
	# 		else:
	# 			return False

	# def get_percent_down(self):
	# 	return (self.january_price - self.latest_price) / self.january_price

class Tickers:
	def __init__(self, market):
		self.market = str(market) # ETF|MUTUAL_FUND|COMMODITY|INDEX|CRYPTO|FOREX|TSX|AMEX|NASDAQ|NYSE|EURONEXT

	def get_all_tickers(self):
		"""Returns the list of symbols for each exchange"""
		try:
			r = requests.get('https://financialmodelingprep.com/api/v3/search?query=&exchange=' + self.market + '&apikey=330d2c5a870ebbea33644948eeeaadf0')
		except Exception as e:
			print(e)
		else:
			tickers = []
			for item in json.loads(r.text):
				tickers.append(str(item['symbol']))

		return tickers

class Strategy():
	def __init__(self, run_date, ticker, company, market_cap, target, \
		market, discount_from_jan, \
		discount_from_target, cap_size, strategy):

		self.ticker = ticker
		self.company = company
		self.market_cap = market_cap
		self.target = target
		self.market = market
		self.discount_from_jan = discount_from_jan
		self.discount_from_target = discount_from_target
		self.cap_size = cap_size
		self.strategy = strategy
		self.date_label = run_date
		self.document_name = (self.date_label \
			+ '_' \
			+ str(self.market) \
			+ '_' \
			+ str(self.strategy) \
			+ '_' \
			+ str(cap_size) \
			+ '_cap_size_' \
			+ str(100 * self.discount_from_jan) \
			+ '_percent_from_jan' \
			+ '_' \
			+ str(100 * self.discount_from_target) \
			+ '_percent_target_difference.txt')

class UnderPricedStocksStrategy(Strategy):
	def execute_strategy(self):
		"""
		This strategy tests:
		1) Is the company market cap a mid-cap
		2) Is the company at least 50% down from january high
		3) Is the company target at least 20% below analyst target
		"""
		if self.is_market_cap_mid_size():
			if self.is_target_at_least_X_percent_higher():
				if self.is_price_at_least_X_percent_down():			
					self.create_record()
				else:
					print('Latest price not sufficiently small')
			else:
				print('Target is not sufficiently high')
		else:
			print('Market cap is not sufficiently small')

	def is_market_cap_mid_size(self):
		if self.market_cap <= float(self.cap_size):
			return True
		else:
			return False

	def is_target_at_least_X_percent_higher(self):
		self.latest_price, self.january_price = self.company.get_january_price_and_latest_price()
		print('Latest price is: ', self.latest_price)
		print('January price is: ', self.january_price)
		if self.target != 0:
			if (self.target - self.latest_price) / self.latest_price >= self.discount_from_target:
				return True
			else:
				return False
		else:
			return False

	def is_price_at_least_X_percent_down(self):
		self.percent_down = (self.january_price - self.latest_price) / self.january_price
		print('Percent down is: ', self.percent_down)
		if self.percent_down >= self.discount_from_jan:
			return True
		else:
			return False

	def create_record(self):
		"""Opens the document and werites info"""
		f = open('runs/' + self.document_name, "a+")
		f.write("{} {} {} {} {}\r".format(self.ticker, self.market_cap, self.latest_price, self.target, self.percent_down))
		print("#####################################################Created record for {}".format(self.ticker))
		f.close()

# class OverPricedStocksStrategy(Strategy):
# 	def execute_strategy(self):
# 		"""
# 		This strategy tests:
# 		1) Is the company market cap a mid-cap
# 		2) Is the company at least 50% down from january high
# 		3) Is the company target at least 20% below analyst target
# 		"""
# 		if (self.is_market_cap_mid_size() and \
# 			self.is_price_at_most_X_percent_down() and \
# 			self.is_company_target_at_least_X_percent_higher_than_target()):
# 			self.create_record()

# 	def is_market_cap_mid_size(self):
# 		if self.market_cap <= float(self.mid_cap_size):
# 			return True
# 		else:
# 			return False

# 	def is_price_at_most_X_percent_down(self):
# 		if self.percent_down <= self.discount_from_jan:
# 			return True
# 		else:
# 			return False

# 	def is_company_target_at_least_X_percent_higher_than_target(self):
# 		if self.target == 0:
# 			return True
# 		else:
# 			if (self.latest_price - self.target) / self.target >= self.discount_from_target:
# 				return True
# 			else:
# 				return False

# 	def create_record(self):
# 		"""Opens the document and werites info"""
# 		f = open(self.document_name, "a+")
# 		f.write("{} | {} | {} | {} | {}\r".format(self.symbol, self.market_cap, self.latest_price, self.target, self.percent_down))
# 		print("#####################################################Created record for {}".format(self.symbol))
# 		f.close()

# class OnePennyStocksStrategy():
# 	def __init__(self, symbol, latest_price):
# 		self.symbol = symbol
# 		self.latest_price = latest_price
# 		self.document_name = '1c_stocks.txt'

# 	def execute_strategy(self):
# 		"""
# 		This strategy tests:
# 		1) If the latest price of the company is 1c
# 		"""
# 		if self.is_latest_price_1c():
# 			self.create_record()

# 	def is_latest_price_1c(self):
# 		if self.latest_price == 0.01:
# 			return True
# 		else:
# 			return False

# 	def create_record(self):
# 		"""Opens the document and werites info"""
# 		f = open(self.document_name, "a+")
# 		f.write("{} | {}\r".format(self.symbol, self.latest_price))
# 		print("#####################################################Created record for {}".format(self.symbol))
# 		f.close()

# class ThreePennyStocksStrategy():
# 	def __init__(self, symbol, latest_price):
# 		self.symbol = symbol
# 		self.latest_price = latest_price
# 		self.document_name = '3c_stocks.txt'

# 	def execute_strategy(self):
# 		"""
# 		This strategy tests:
# 		1) If the latest price of the company is 1c
# 		"""
# 		if self.is_latest_price_less_than_3c():
# 			self.create_record()

# 	def is_latest_price_less_than_3c(self):
# 		if self.latest_price <= 0.03:
# 			return True
# 		else:
# 			return False

# 	def create_record(self):
# 		"""Opens the document and werites info"""
# 		f = open(self.document_name, "a+")
# 		f.write("{} | {}\r".format(self.symbol, self.latest_price))
# 		print("#####################################################Created record for {}".format(self.symbol))
# 		f.close()
