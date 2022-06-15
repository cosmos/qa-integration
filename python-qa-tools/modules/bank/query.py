import os, json

from utils import exec_command
from stats import QUERY_TYPE

DAEMON = os.getenv("DAEMON")
RPC = os.getenv("RPC")

# query_balances returns the balance json by taking bech32 address as parameter.
def query_balances(address, test_type=None):
    try:
        command = f"{DAEMON} q bank balances {address} --node {RPC} --output json"
        balance, balanceerr = exec_command(command, test_type, QUERY_TYPE)
        if len(balanceerr):
            return False, balanceerr
        return True, json.loads(balance)
    except Exception as e:
        return False, e
