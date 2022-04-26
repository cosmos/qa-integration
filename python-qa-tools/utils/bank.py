import json, os
from tokenize import String
from utils.commands import command_processor

DAEMON = os.getenv('DAEMON')

def print_balance_deductions(wallet, diff):
    if diff > 0:
        print(f"Balance in the {wallet} increased by {diff}")
    elif diff < 0:
        print(f"Balance in the {wallet} decreased by {-1 * diff}")
    else:
        print(f"No deduction from {wallet} balance")

def balance_query(bech_address: String, RPC : String):
    command = f"{DAEMON} q bank balances {bech_address} --node {RPC} --output json"
    balance, balanceerr = command_processor(command)
    balance = json.loads(balance)
    balance = int(balance['balances'][0]['amount'])
    return balance, balanceerr

def fetch_balance_json(account: String, RPC: String):
    command = f"{DAEMON} q bank balances {account} --node {RPC} --output json"
    balance, balanceerr = command_processor(command)
    return json.loads(balance), balanceerr

def query_account(account, RPC):
    command = f"{DAEMON} q account {account} --node {RPC} --output json"
    stdout, stderr = command_processor(command)
    return json.loads(stdout), stderr