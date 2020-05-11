import requests
import json
import time
from analyst_utility_classes import Company, Symbols, UnderpricedStocksStrategy, OverpricedStocksStrategy
from support_functions import get_input_args

def main():
	market = get_input_args().market
	strategy_to_run = get_input_args().strategy

	#symbols = ['SHOP', 'TSLA']
	symbols = Symbols(market).get_all_symbols()
	print('{} size is {} companies long'.format(market, len(symbols)))

	for symbol in symbols:
		print('------------------------------------------------------' \
			'---Processing {} number {} from {}'.format(symbol, symbols.index(symbol), len(symbols)))
		company = Company(symbol)
		try:
			market_cap = company.get_market_cap()
			print('Market cap is {}'.format(market_cap))
			latest_price = company.get_latest_price()
			print('Latest price is {}'.format(latest_price))
			jan_price = company.get_january_price()
			print('January price is {}'.format(jan_price))
			percent_down = company.get_percent_down()
			print('Percent down is {}'.format(percent_down))
			target = company.get_1_year_target()
			print('Target is {}'.format(target))
		except Exception as e:
			print(e)
		else:
			if strategy_to_run == 'underpriced':
				discount_from_jan = 0.5
				discount_from_target = 0.20
				mid_cap_size = 500000000
				sleep_time = 1
				UnderpricedStocksStrategy(symbol, market_cap, target, latest_price, jan_price, \
					market, percent_down, discount_from_jan, \
					discount_from_target, mid_cap_size, strategy_to_run).execute_strategy()
				time.sleep(sleep_time)
			elif strategy_to_run == 'overpriced':
				discount_from_jan = 0.05
				discount_from_target = 0.30
				mid_cap_size = 500000000
				sleep_time = 1
				OverpricedStocksStrategy(symbol, market_cap, target, latest_price, jan_price, \
					market, percent_down, discount_from_jan, \
					discount_from_target, mid_cap_size, strategy_to_run).execute_strategy()
				time.sleep(sleep_time)

if __name__ == '__main__':
	main()
