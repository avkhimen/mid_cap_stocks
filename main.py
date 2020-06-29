import requests
import json
import time
from analyst_utility_classes import Company, Tickers, UnderPricedStocksStrategy #, OverPricedStocksStrategy, OnePennyStocksStrategy, ThreePennyStocksStrategy
from support_functions import get_input_args, get_market_tickers, get_datetime

def main():
	market = get_input_args().market
	strategy_to_run = get_input_args().strategy
	start_index = get_input_args().start_index
	run_date = get_datetime()

	#tickers = ['GTE', 'MOGO.TO']
	#tickers = Symbols(market).get_all_symbols()
	tickers = get_market_tickers(market)
	print('{} size is {} companies long'.format(market, len(tickers)))

	for ticker in tickers[start_index:]:
		print('------------------------------------------------------' \
			'---Processing {} number {} from {}'.format(ticker, tickers.index(ticker), len(tickers)))
		company = Company(ticker)
		try:
			market_cap, target = company.get_1yr_target_and_market_cap()
			#market_cap = company.get_market_cap()
			print('Market cap is {}'.format(market_cap))
			print('Target is {}'.format(target))
			# latest_price = company.get_latest_price()
			# print('Latest price is {}'.format(latest_price))
			# jan_price = company.get_january_price()
			# print('January price is {}'.format(jan_price))
			# percent_down = company.get_percent_down()
			# print('Percent down is {}'.format(percent_down))
			#target = company.get_1_year_target()
			#print('Target is {}'.format(target))
		except Exception as e:
			print(e)
		else:
			if strategy_to_run == 'underpriced':
				discount_from_jan = 0.5
				discount_from_target = 1
				cap_size = 500000000
				sleep_time = 0
				UnderPricedStocksStrategy(run_date, ticker, company, market_cap, target, \
					market, discount_from_jan, discount_from_target, \
					cap_size, strategy_to_run).execute_strategy()
				time.sleep(sleep_time)
			# elif strategy_to_run == 'overpriced':
			# 	discount_from_jan = 0.5
			# 	discount_from_target = 1
			# 	mid_cap_size = 500000000
			# 	sleep_time = 1
			# 	OverPricedStocksStrategy(ticker, market_cap, target, latest_price, jan_price, \
			# 		market, percent_down, discount_from_jan, \
			# 		discount_from_target, mid_cap_size, strategy_to_run).execute_strategy()
			# 	time.sleep(sleep_time)
			# elif strategy_to_run == 'penny':
			# 	latest_price = company.get_latest_price()
			# 	print('Latest price is {}'.format(latest_price))
			# 	sleep_time = 0
			# 	OnePennyStocksStrategy(ticker, latest_price).execute_strategy()
			# 	time.sleep(sleep_time)
			# elif strategy_to_run == '3penny':
			# 	latest_price = company.get_latest_price()
			# 	print('Latest price is {}'.format(latest_price))
			# 	sleep_time = 0
			# 	ThreePennyStocksStrategy(ticker, latest_price).execute_strategy()
			# 	time.sleep(sleep_time)

if __name__ == '__main__':
	main()
