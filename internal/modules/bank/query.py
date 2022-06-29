import os, json

from utils import exec_command

DAEMON = os.getenv("DAEMON")
RPC = os.getenv("RPC")

# query_balances returns the balance json by taking bech32 address as parameter.
def query_balances(address):
    try:
        command = f"{DAEMON} q bank balances {address} --node {RPC} --output json"
        balance, balance_err = exec_command(command)
        if len(balance_err):
            return False, balance_err
        return True, json.loads(balance)
    except Exception as e:
        return False, e
