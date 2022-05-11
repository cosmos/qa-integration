import os, json
from utils.commands import exec_command

DAEMON = os.getenv('DAEMON')
RPC = os.getenv('RPC')

def query_balances(address):
    try:
        command = f"{DAEMON} q bank balances {address} --node {RPC} --output json"
        balance, balanceerr = exec_command(command)
        if len(balanceerr):
            return False, balanceerr
        return True, json.loads(balance)
    except Exception as e:
        return False, e