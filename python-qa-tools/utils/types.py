import argparse
from core.keys import keys_show
from modules.auth.query import query_account

def account_type(address):
    status, response = query_account(address)
    if not status:
        raise argparse.ArgumentTypeError(response)
    return address

def num_txs_type(x):
    if int(x) < 1000:
        raise argparse.ArgumentTypeError('The argument NUM_TXS should be 1000 or more')
    return int(x)

def node_type(x):
    x = int(x)
    if x < 2:
        raise argparse.ArgumentTypeError(f"The number of nodes should be atleast 2, you have entered {x}")
    return x
