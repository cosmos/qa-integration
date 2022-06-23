from distutils import text_file
import json, os
import re
from utils import exec_command, execute_tx_by_type
from modules.staking.query import (
    get_public_key,
)

DAEMON = os.getenv("DAEMON")
DENOM = os.getenv("DENOM")
CHAINID = os.getenv("CHAINID")
HOME = os.getenv("HOME")
DAEMON_HOME = os.getenv("DAEMON_HOME")
RPC = os.getenv("RPC")
DEFAULT_GAS = 2000000

# tx_delegate function internally calls the 'delegate tx' command and return the response in json format.
def tx_delegate(from_key, validator_addr, amount, gas=DEFAULT_GAS):
    command = f"{DAEMON} tx staking delegate {validator_addr} {amount}{DENOM} --from {from_key} --chain-id {CHAINID} --output json --node {RPC} --gas {gas}"
    status, res = execute_tx_by_type(command)
    return status, res


# tx_redelegate function internally calls the 'redelegate tx' command and return the response in json format.
def tx_redelegate(
    from_key,
    src_validator_addr,
    dst_validator_addr,
    amount,
    gas=DEFAULT_GAS,
):

    command = f"{DAEMON} tx staking redelegate {src_validator_addr} {dst_validator_addr} {amount}{DENOM} --from {from_key} --chain-id {CHAINID} --output json --node {RPC} --gas {gas}"
    status, res = execute_tx_by_type(command)
    return status, res


# tx_unbond function internally calls the 'unbond tx' command and return the response in json format.
def tx_unbond(from_key, validator_addr, amount, gas=DEFAULT_GAS):
    command = f"{DAEMON} tx staking unbond {validator_addr} {amount}{DENOM} --from {from_key} --chain-id {CHAINID} --output json --node {RPC} --gas {gas}"
    status, res = execute_tx_by_type(command)
    return status, res


# tx_create_validator is to create new validator initialized with a self-delegation to it.
def tx_create_validator(
    from_key, amount, moniker, temp_dir, gas=DEFAULT_GAS, unsigned=False, sequence=None
):
    try:
        public_key, err = get_public_key(temp_dir)
        if err:
            return False, err

        if unsigned:
            command = f"{DAEMON} tx staking create-validator --amount {amount}{DENOM} --commission-max-change-rate 0.1 --commission-max-rate 0.2 --commission-rate 0.1 --from {from_key} --min-self-delegation 1 --moniker {moniker} --pubkey {public_key}  --chain-id {CHAINID} -y"
            tx, tx_err = exec_command(command)
            if len(tx_err):
                return False, tx_err
            return True, json.loads(tx)
        else:
            if sequence is not None:
                command = f"{DAEMON} tx staking create-validator --amount {amount}{DENOM} --commission-max-change-rate 0.1 --commission-max-rate 0.2 --commission-rate 0.1 --from {from_key} --min-self-delegation 1 --moniker {moniker} --pubkey {public_key}  --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --sequence {sequence} --gas {gas}"

            else:
                command = f"{DAEMON} tx staking create-validator --amount {amount}{DENOM} --commission-max-change-rate 0.1 --commission-max-rate 0.2 --commission-rate 0.1 --from {from_key} --min-self-delegation 1 --moniker {moniker} --pubkey {public_key}  --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --gas {gas}"
            tx, tx_err = exec_command(command)
            tx = json.loads(tx)
            if len(tx_err):
                return False, tx_err
            elif tx["code"] != 0:
                return False, tx
            return True, tx
    except Exception as e:
        return False, e
