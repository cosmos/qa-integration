import json, os
from utils.commands import exec_command
DAEMON = os.getenv('DAEMON')
DENOM = os.getenv('DENOM')
CHAINID = os.getenv('CHAINID')
HOME = os.getenv('HOME')
DAEMON_HOME = os.getenv('DAEMON_HOME')
RPC = os.getenv('RPC')

def tx_send(from_address, to_address, amount, gas, unsigned = False, sequence = None):
    try:    
        if unsigned:
            command = f"{DAEMON} tx bank send {from_address} {to_address} {amount}{DENOM} --chain-id {CHAINID} --output json --generate-only --gas {gas}"
            Tx, Txerr = exec_command(command)
            if len(Txerr):
                return False, Txerr
            return True, json.loads(Tx)
        else:
            if sequence != None:
                command = f"{DAEMON} tx bank send {from_address} {to_address} {amount}{DENOM} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --sequence {sequence}"
                
            else:
                command = f"{DAEMON} tx bank send {from_address} {to_address} {amount}{DENOM} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y"
            Tx, Txerr = exec_command(command)
            Tx = json.loads(Tx)
            if len(Txerr):
                return False, Txerr
            elif Tx['code'] != 0:
                return False, Tx
            return True, Tx
    except Exception as e:
        return False, e