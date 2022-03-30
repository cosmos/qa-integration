from dotenv import dotenv_values
from utils.commands import command_processor

config = dotenv_values('.env')
DAEMON = config['DAEMON']
DAEMON_HOME = config['DAEMON_HOME']

def fetch_bech_address(account_name):
    command = f"{DAEMON} keys show {account_name} -a --home {DAEMON_HOME}-1 --keyring-backend test" 
    return command_processor(command)