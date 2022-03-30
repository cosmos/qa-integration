import argparse, json
from utils.keys import fetch_bech_address

def account_type(x):
    _stdout, stderr = fetch_bech_address(f"account{x}")
    if len(stderr):
        raise argparse.ArgumentTypeError(stderr)
    return int(x)

def num_txs_type(x):
    if int(x) < 1000:
        raise argparse.ArgumentTypeError('The argument NUM_TXS should be 1000 or more')
    return int(x)

def write_json(file_name):
    with open(file_name, 'r+') as file:
            file_data = json.load(file)
            new_data = file_data["body"]["messages"][-1]
            file_data["body"]["messages"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent = 4)

def node_type(x):
    x = int(x)
    if x < 2:
        raise argparse.ArgumentTypeError(f"The number of nodes should be Min. 2, you have entered {x}")
    return x
