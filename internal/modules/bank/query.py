import os, json

from utils import exec_command, env

DAEMON = env.DAEMON
RPC = env.RPC

# query_balances returns the balance json by taking bech32 address as parameter.
def query_balances(address):
    try:
        command = f"{DAEMON} q bank balances {address} --node {RPC} --output json"
        balance, balanceerr = exec_command(command)
        if len(balanceerr):
            return False, balanceerr
        return True, json.loads(balance)
    except Exception as e:
        return False, e
