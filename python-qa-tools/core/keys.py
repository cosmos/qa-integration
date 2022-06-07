"""
This page contains all the functions calling keys sub-commands
"""
import os
import json
from utils import exec_command

DAEMON = os.getenv('DAEMON')
DAEMON_HOME = os.getenv('DAEMON_HOME')

def keys_show(account, account_type="acc"):
    """The function `keys_show` will return the key details in json format.
    """
    try:
        command = f'''{DAEMON} keys show {account} --home {DAEMON_HOME}-1 --bech {account_type}
        --keyring-backend test --output json'''
        stdout, stderr = exec_command(command)
        if len(stderr) != 0:
            return False, stderr
        return True, json.loads(stdout)
    except Exception as error: # pylint: disable=broad-except
        return False, error
    