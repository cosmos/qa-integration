import argparse, os, json

from utils import exec_command
from stats import QUERY_TYPE

DAEMON = os.getenv("DAEMON")
RPC = os.getenv("RPC")

# account_type is an user-defined data type used to validate account addresses read from Argument Parser.
def account_type(address, test_type=None):
    status, response = query_account(address, test_type)
    if not status:
        raise argparse.ArgumentTypeError(response)
    return address


# query_account function will take the bech32 address as input and output the information of account.
def query_account(address, test_type=None):
    try:
        command = f"{DAEMON} query auth account {address} --node {RPC} --output json"
        stdout, stderr = exec_command(command, test_type, QUERY_TYPE)
        if len(stderr):
            return False, stderr
        return True, json.loads(stdout)
    except Exception as e:
        return False, e
