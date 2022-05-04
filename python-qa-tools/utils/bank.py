import json, os
from utils.commands import exec_command

DAEMON = os.getenv('DAEMON')

def print_balance_deductions(wallet, diff):
    if diff > 0:
        print(f"Balance in the {wallet} increased by {diff}")
    elif diff < 0:
        print(f"Balance in the {wallet} decreased by {-1 * diff}")
    else:
        print(f"No deduction from {wallet} balance")

def query_account(account, RPC):
    command = f"{DAEMON} q account {account} --node {RPC} --output json"
    stdout, stderr = exec_command(command)
    return json.loads(stdout), stderr