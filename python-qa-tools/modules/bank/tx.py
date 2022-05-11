import json, os
from utils.commands import exec_command
DAEMON = os.getenv('DAEMON')
DENOM = os.getenv('DENOM')
CHAINID = os.getenv('DENOM')
HOME = os.getenv('HOME')
DAEMON_HOME = os.getenv('DAEMON_HOME')
RPC = os.getenv('RPC')

def tx_send(from_address, to_address, amount, gas, unsigned = False, sequence = None):
    try:    
        if unsigned:
            command = f"{DAEMON} tx bank send {from_address} {to_address} {amount}{DENOM} --keyring-backend test --chain-id {CHAINID} --generate-only --gas {gas} --output json"
        else:
            if sequence:
                command = f"{DAEMON} tx bank send {from_address} {to_address} {amount}{DENOM} --home {DAEMON_HOME}-1 --keyring-backend test --chain-id {CHAINID} --sequence {sequence} --node {RPC} --output json --gas {gas} -y"
            else:
                command = f"{DAEMON} tx bank send {from_address} {to_address} {amount}{DENOM} --home {DAEMON_HOME}-1 --keyring-backend test --chain-id {CHAINID} --node {RPC} --output json --gas {gas}-y"
        Tx, Txerr = exec_command(command)
        if len(Txerr):
            return False, Txerr
        return True, json.loads(Tx)
    except Exception as e:
        return False, e