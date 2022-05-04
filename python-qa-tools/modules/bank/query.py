import os, json
from utils.commands import exec_command

DAEMON = os.getenv('DAEMON')
def query_balances(address, RPC, amount = False):
    command = f"{DAEMON} q bank balances {address} --node {RPC} --output json"
    balance, balanceerr = exec_command(command)
    balance = json.loads(balance)
    if amount:
        balance = int(balance['balances'][0]['amount'])
    return balance, balanceerr