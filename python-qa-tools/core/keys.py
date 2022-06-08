import os, json

from utils import exec_command

DAEMON = os.getenv('DAEMON')
DAEMON_HOME = os.getenv('DAEMON_HOME')
PATH = os.getenv('PATH')

# The function `keys_show` will return the key details in json format.
def keys_show(account, type = "acc"):
    try:
        print(f"Path...{PATH}")
        bashout, basherr = exec_command(f"cat ~/.bashrc")
        print(f"Bash...StdOut...{bashout}....StdErr...{basherr}")
        command = f"{DAEMON} keys show {account} --home {DAEMON_HOME}-1 --bech {type} --keyring-backend test --output json"
        stdout, stderr = exec_command(command)
        print(f"Output...StdOut...{stdout}....StdErr...{stderr}")
        if len(stderr):
            return False, stderr
        return True, json.loads(stdout)
    except Exception as e:
        return False, e
