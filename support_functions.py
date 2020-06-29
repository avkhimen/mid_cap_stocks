import argparse
import pandas as pd
import numpy as np
from datetime import datetime

def get_input_args():
    """
    Returns input arguments for main file execution
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--market', type = str, default = 'TSX', 
                        help = 'Market to get stocks from')
    parser.add_argument('--strategy', type = str, default = 'underpriced', 
                        help = 'Strategy to run')
    parser.add_argument('--start_index', type = int, default = 0, 
                        help = 'Start index of the ticker')
    return parser.parse_args()

def get_market_tickers(market):
	"""
	Returns the tickers for the specific market
	"""
	data = np.load('tickers/' + market.lower() + '_tickers.npy')
	tickers = data.tolist()
	return tickers

def get_datetime():
	"""
	Returns current date and time in the format dd/mm/YY H:M:S
	"""
	now = datetime.now()
	dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
	
	return dt_string	