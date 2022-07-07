from cgi import print_arguments
from utils import exec_command
import os
import json

DAEMON = os.getenv('DAEMON')
DENOM = os.getenv('DENOM')
DEFAULT_GAS = 2000000
CHAINID = os.getenv('CHAINID')
RPC = os.getenv('RPC')
DAEMON_HOME = os.getenv('DAEMON_HOME')


def tx_withdraw_rewards(from_key,validator_addr,gas={DEFAULT_GAS},unsigned = False,sequence = None):
    try:
        if unsigned:
            command = f"{DAEMON} tx distribution withdraw-rewards {validator_addr} --from {from_key} --chain-id {CHAINID} --output json --node {RPC}"
            tx, tx_err = exec_command(command)
            if len(tx_err):
                return False,tx_err
            return True, json.loads(tx)
        else: 
            if sequence is not None:
                command = f"{DAEMON} tx distribution withdraw-rewards {validator_addr} --from {from_key} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --sequence {sequence}"

            else:
                 command = f"{DAEMON} tx distribution withdraw-rewards {validator_addr} --from {from_key} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y"
            tx, tx_err = exec_command(command)
            tx = json.loads(tx)
            if len(tx_err):
                return False, tx_err
            elif tx['code'] != 0:
                return False,tx 
            return True,tx
    except Exception as e:
        return False,e

def tx_withdraw_commision_rewards(from_key,validator_addr,gas={DEFAULT_GAS},unsigned = False,sequence = None):
    try:
        if unsigned:
            command = f"{DAEMON} tx distribution withdraw-rewards {validator_addr} --from {from_key} --commission --chain-id {CHAINID} --output json --node {RPC} --generate-only --gas {gas}"
            tx, tx_err = exec_command(command)
            if len(tx_err):
                return False,tx_err
            return True, json.loads(tx)
        else: 
            if sequence is not None:
                command = f"{DAEMON} tx distribution withdraw-rewards {validator_addr} --from {from_key} --commission --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --sequence {sequence} --gas {gas}"

            else:
                 command = f"{DAEMON} tx distribution withdraw-rewards {validator_addr} --from {from_key} --commission --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y"
            tx, tx_err = exec_command(command)
            tx = json.loads(tx)
            if len(tx_err):
                return False, tx_err
            elif tx['code'] != 0:
                return False,tx 
            return True,tx
    except Exception as e:
        return False,e


def tx_withdraw_allrewards(from_key,gas={DEFAULT_GAS},unsigned = False,sequence = None):
    try:
        if unsigned:
            command = f"{DAEMON} tx distribution withdraw-all-rewards --from {from_key} --chain-id {CHAINID} --output json --node {RPC} --generate-only --gas {gas}"
            tx, tx_err = exec_command(command)
            if len(tx_err):
                return False, tx_err
            return True, json.loads(tx)
        else:
            if sequence is not None:
                command = f"{DAEMON} tx distribution withdraw-all-rewards --from {from_key} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --sequence {sequence}"
            else:
                command = f"{DAEMON} tx distribution withdraw-all-rewards --from {from_key} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y"
            tx, tx_err = exec_command(command)
            tx = json.loads(tx)
            if len(tx_err):
                return False, tx_err
            elif tx['code'] != 0:
                return False,tx 
            return True,tx
    except Exception as e:
        return False,e

def tx_fund_communitypool(from_key,amount,gas={DEFAULT_GAS},unsigned = False,sequence = None):
    try:
        if unsigned:
            command = f"{DAEMON} tx distribution fund-community-pool {amount}{DENOM} --from {from_key} --chain-id {CHAINID} --output json --node {RPC} --generate-only"
            tx, tx_err = exec_command(command)
            if len(tx_err):
                return False, tx_err
            return True, json.loads(tx)
        else:
            if sequence is not None:
                command = f"{DAEMON} tx distribution fund-community-pool {amount}{DENOM} --from {from_key} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --sequence {sequence}"
            else:
                command = f"{DAEMON} tx distribution fund-community-pool {amount}{DENOM} --from {from_key} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y"
            tx, tx_err = exec_command(command)
            tx = json.loads(tx)
            if len(tx_err):
                return False, tx_err
            elif tx['code'] != 0:
                return False,tx 
            return True,tx
    except Exception as e:
        return False,e

def tx_withdraw_addr(from_key,withdraw_addr,gas={DEFAULT_GAS},unsigned = False,sequence = None):
    try:
        if unsigned:
            command = f"{DAEMON} tx distribution set-withdraw-addr {withdraw_addr} --from {from_key} --chain-id {CHAINID} --output json --node {RPC} --generate-only --output json"
            tx, tx_err = exec_command(command)
            if len(tx_err):
                return False, tx_err
            return True, json.loads(tx)
        else:
            if sequence is not None:
                command = f"{DAEMON} tx distribution set-withdraw-addr {withdraw_addr} --from {from_key} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --sequence {sequence}"
            else:
                command = f"{DAEMON} tx distribution set-withdraw-addr {withdraw_addr} --from {from_key} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y"
                tx, tx_err = exec_command(command)
                tx = json.loads(tx)
                if len(tx_err):
                    print(tx_err)
                    return False, tx_err
                elif tx['code'] != 0:
                    return False,tx 
                return True,tx
    except Exception as e:
        return False,e

# tx_delegate function internally calls the 'delegate tx' command and return the response in json format.
def tx_delegate(from_key, validator_addr, amount, gas=DEFAULT_GAS):
    command = f"{DAEMON} tx staking delegate {validator_addr} {amount}{DENOM} --from {from_key} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --output json -y --node {RPC} --gas {gas}"
    tx, tx_err = exec_command(command)
    if len(tx_err):
        return False, tx_err
    return True, json.loads(tx)