import argparse, os, json

from utils import exec_command

DAEMON = os.getenv('DAEMON')
RPC = os.getenv('RPC')

# query account function will take the bech32 address as input and output the information of account.

def account_type(address):
    status, response = query_account(address)
    if not status:
        raise argparse.ArgumentTypeError(response)
    return address

def query_account(address):
    try:
        command = f"{DAEMON} query auth account {address} --node {RPC} --output json"
        stdout, stderr = exec_command(command)
        if len(stderr):
            return False, stderr
        return True, json.loads(stdout)
    except Exception as e:
        return False, e