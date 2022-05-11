import os, json
from utils.commands import exec_command

DAEMON = os.getenv('DAEMON')
DAEMON_HOME = os.getenv('DAEMON_HOME')

def keys_show(account, type = None):
    try:
        if type == "val":
            command = f"{DAEMON} keys show {account} --home {DAEMON_HOME}-1 --bech val --keyring-backend test --output json"
        else:
            command = f"{DAEMON} keys show {account} --home {DAEMON_HOME}-1 --keyring-backend test --output json"
        stdout, stderr = exec_command(command)
        if len(stderr):
            return False, stderr
        return True, json.loads(stdout)
    except Exception as e:
        return False, e