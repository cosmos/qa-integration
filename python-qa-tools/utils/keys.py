import os
from utils.commands import command_processor

DAEMON = os.getenv('DAEMON')
DAEMON_HOME = os.getenv('DAEMON_HOME')

def fetch_account_address(account_name):
    command = f"{DAEMON} keys show {account_name} -a --home {DAEMON_HOME}-1 --keyring-backend test" 
    return command_processor(command)

def fetch_validator_address(validator_name, type=None):
    if not type:
        command = f"{DAEMON} keys show {validator_name} -a --home {DAEMON_HOME}-1 --keyring-backend test" 
    elif type == "bech":
        command = f"{DAEMON} keys show {validator_name} -a --bech val --home {DAEMON_HOME}-1 --keyring-backend test"
    return command_processor(command)
        