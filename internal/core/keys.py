import os, json

from utils import exec_command

DAEMON = os.getenv("DAEMON")
DAEMON_HOME = os.getenv("DAEMON_HOME")

# The function `keys_show` will return the key details in json format.
def keys_show(account, type="acc", home=1):
    try:
        command = f"{DAEMON} keys show {account} --home {DAEMON_HOME}-{home} --bech {type} --keyring-backend test --output json"
        stdout, stderr = exec_command(command)
        if len(stderr):
            return False, stderr
        return True, json.loads(stdout)
    except Exception as e:
        return False, e
