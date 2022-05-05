import os
from utils.commands import exec_command

DAEMON = os.getenv('DAEMON')
DAEMON_HOME = os.getenv('DAEMON_HOME')

def fetch_account_address(account_name, type=None):
    if not type:
        command = f"{DAEMON} keys show {account_name} -a --home {DAEMON_HOME}-1 --keyring-backend test"
    elif type == "validator":
        command = f"{DAEMON} keys show {account_name} -a --bech val --home {DAEMON_HOME}-1 --keyring-backend test"
    return exec_command(command)
        