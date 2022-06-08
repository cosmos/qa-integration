from distutils import text_file
import json, os
from utils import exec_command

DAEMON = os.getenv('DAEMON')
DENOM = os.getenv('DENOM')
CHAINID = os.getenv('CHAINID')
HOME = os.getenv('HOME')
DAEMON_HOME = os.getenv('DAEMON_HOME')
RPC = os.getenv('RPC')
DEFAULT_GAS = 2000000

# tx_delegate function internally calls the 'delegate tx' command and return the response in json format.
def tx_delegate(from_key, to_address, amount,fee, gas="auto", unsigned = False, sequence = None):
    try:    
        if unsigned:
            command = f"{DAEMON} tx staking delegate {to_address} {amount}{DENOM} --from {from_key} --fees {fee}{DENOM} --chain-id {CHAINID} --output json --node {RPC} --generate-only --gas {gas}"
            tx, tx_err = exec_command(command)
            if len(tx_err):
                return False, tx_err
            return True, json.loads(tx)
        else:
            if sequence is not None:
                command = f"{DAEMON} tx staking delegate {to_address} {amount}{DENOM} --from {from_key} --fees {fee}{DENOM} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --sequence {sequence} --gas {gas}"
                
            else:
                command = f"{DAEMON}  tx staking delegate {to_address} {amount}{DENOM} --from {from_key} --fees {fee}{DENOM} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --gas {gas}"
            tx, tx_err = exec_command(command)
            tx = json.loads(tx)
            if len(text_file):
                return False, tx_err
            elif tx['code'] != 0:
                return False, tx
            return True, tx
    except Exception as e:
        return False, e

# tx_redelegate function internally calls the 'redelegate tx' command and return the response in json format.
def tx_redelegate(from_key,from_address, to_address, amount,fee, gas="auto", unsigned = False, sequence = None):
    try:    
        if unsigned:
            command = f"{DAEMON} tx staking redelegate {from_address} {to_address} {amount}{DENOM} --from {from_key} --fees {fee}{DENOM} --chain-id {CHAINID} --output json --node {RPC} --generate-only --gas {gas}"
            tx, tx_err = exec_command(command)
            if len(tx_err):
                return False, tx_err
            return True, json.loads(tx)
        else:
            if sequence is not None:
                command = f"{DAEMON} tx staking redelegate {from_address} {to_address} {amount}{DENOM} --from {from_key} --fees {fee}{DENOM} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --sequence {sequence} --gas {gas}"
                
            else:
                command = f"{DAEMON}  tx staking redelegate {from_address} {to_address} {amount}{DENOM} --from {from_key} --fees {fee}{DENOM} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --gas {gas}"
            tx, tx_err = exec_command(command)
            tx = json.loads(tx)
            if len(text_file):
                return False, tx_err
            elif tx['code'] != 0:
                return False, tx
            return True, tx
    except Exception as e:
        return False, e