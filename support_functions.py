import argparse

def get_input_args():
    """Returns input arguments for main file execution"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--market', type = str, default = 'TSX', 
                        help = 'Market to get stocks from')
    parser.add_argument('--strategy', type = str, default = 'overpriced', 
                        help = 'Strategy to run')
    return parser.parse_args()