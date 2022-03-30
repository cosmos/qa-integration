import json
from dotenv import dotenv_values
from utils.commands import command_processor

config = dotenv_values('.env')
DAEMON = config['DAEMON']

def print_balance_deductions(wallet, diff):
    if diff > 0:
        print(f"Balance in the {wallet} increased by {diff}")
    elif diff < 0:
        print(f"Balance in the {wallet} decreased by {-1 * diff}")
    else:
        print(f"No deduction from {wallet} balance")

def balance_query(bech_address, RPC):
    command = f"{DAEMON} q bank balances {bech_address} --node {RPC} --output json"
    balance, balanceerr = command_processor(command)
    balance = json.loads(balance)
    balance = int(balance['balances'][0]['amount'])
    return balance, balanceerr