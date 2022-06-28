import json

from utils import exec_command, env

DAEMON = env.DAEMON
DAEMON_HOME = env.DAEMON_HOME

# The function `keys_show` will return the key details in json format.
def keys_show(account, type="acc"):
    try:
        command = f"{DAEMON} keys show {account} --home {DAEMON_HOME}-1 --bech {type} --keyring-backend test --output json"
        stdout, stderr = exec_command(command)
        if len(stderr):
            return False, stderr
        return True, json.loads(stdout)
    except Exception as e:
        return False, e
