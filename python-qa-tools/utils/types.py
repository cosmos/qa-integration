import argparse
from utils.keys import fetch_account_address

def account_type(x):
    _stdout, stderr = fetch_account_address(f"account{x}")
    if len(stderr):
        raise argparse.ArgumentTypeError(stderr)
    return int(x)

def validator_account_type(x):
    _stdout, stderr = fetch_account_address(f"validator{x}")
    if len(stderr):
        raise argparse.ArgumentTypeError(stderr)
    return int(x)

def num_txs_type(x):
    if int(x) < 1000:
        raise argparse.ArgumentTypeError('The argument NUM_TXS should be 1000 or more')
    return int(x)

def node_type(x):
    x = int(x)
    if x < 2:
        raise argparse.ArgumentTypeError(f"The number of nodes should be Min. 2, you have entered {x}")
    return x
