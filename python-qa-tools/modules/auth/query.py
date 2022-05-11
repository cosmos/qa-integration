import os, json
from utils.commands import exec_command

DAEMON = os.getenv('DAEMON')
RPC = os.getenv('RPC')

# query account function will take the bech32 address as input and output the information of account.
def query_account(address):
    try:
        command = f"{DAEMON} query auth account {address} --node {RPC} --output json"
        stdout, stderr = exec_command(command)
        if len(stderr):
            return False, stderr
        return True, json.loads(stdout)
    except Exception as e:
        return False, e