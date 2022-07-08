import json, os
import re
from utils import exec_command
from modules.staking.query import (
    fetch_validator_pubkey_from_node,
)

DAEMON = os.getenv("DAEMON")
DENOM = os.getenv("DENOM")
CHAINID = os.getenv("CHAINID")
HOME = os.getenv("HOME")
DAEMON_HOME = os.getenv("DAEMON_HOME")
RPC = os.getenv("RPC")
DEFAULT_GAS = 2000000

# tx_delegate takes from_key, validator address and amount as paramaters and
# internally executes the 'delegate tx' command and return the response in json format.
def tx_delegate(
    from_key,
    validator_addr,
    amount,
    gas=DEFAULT_GAS,
    unsigned=False,
    sequence=None,
    extra_args="",
):
    try:
        if unsigned:
            command = f"{DAEMON} tx staking delegate {validator_addr} {amount}{DENOM} --from {from_key} --chain-id {CHAINID} --output json --node {RPC} --gas {gas} --generate-only"
            tx, tx_err = exec_command(command)
            if len(tx_err):
                return False, tx_err
            return True, json.loads(tx)
        else:
            if sequence is not None:
                command = f"{DAEMON} tx staking delegate {validator_addr} {amount}{DENOM} --from {from_key} --chain-id {CHAINID} --output json --node {RPC} --gas {gas} --keyring-backend test --home {DAEMON_HOME}-1 -y --sequence {sequence}"

            else:
                command = f"{DAEMON} tx staking delegate {validator_addr} {amount}{DENOM} --from {from_key} --chain-id {CHAINID} --output json --node {RPC} --gas {gas} --keyring-backend test --home {DAEMON_HOME}-1 -y"
            tx, tx_err = exec_command(command)
            tx = json.loads(tx)
            if len(tx_err):
                return False, tx_err
            elif tx["code"] != 0:
                return False, tx
            return True, tx
    except Exception as e:
        return False, e


# tx_redelegate takes from_key, source and disration validator address as params and
# internally executes the 'redelegate tx' command and return the response in json format.
def tx_redelegate(
    from_key,
    src_validator_addr,
    dst_validator_addr,
    amount,
    gas=DEFAULT_GAS,
    unsigned=False,
    sequence=None,
    extra_args="",
):
    try:
        if unsigned:
            command = f"{DAEMON} tx staking redelegate {src_validator_addr} {dst_validator_addr} {amount}{DENOM} --from {from_key} --chain-id {CHAINID} --output json --node {RPC} --gas {gas} --generate-only"
            tx, tx_err = exec_command(command)
            if len(tx_err):
                return False, tx_err
            return True, json.loads(tx)
        else:
            if sequence is not None:
                command = f"{DAEMON} tx staking redelegate {src_validator_addr} {dst_validator_addr} {amount}{DENOM} --from {from_key} --chain-id {CHAINID} --output json --node {RPC} --gas {gas} --keyring-backend test --home {DAEMON_HOME}-1 -y --sequence {sequence}"

            else:
                command = f"{DAEMON} tx staking redelegate {src_validator_addr} {dst_validator_addr} {amount}{DENOM} --from {from_key} --chain-id {CHAINID} --output json --node {RPC} --gas {gas} --keyring-backend test --home {DAEMON_HOME}-1 -y"
            tx, tx_err = exec_command(command)
            tx = json.loads(tx)
            if len(tx_err):
                return False, tx_err
            elif tx["code"] != 0:
                return False, tx
            return True, tx
    except Exception as e:
        return False, e


# tx_unbond takes from key, valiator address and amount as params and
# internally executes the 'unbond tx' command and return the response in json format.
def tx_unbond(
    from_key,
    validator_addr,
    amount,
    gas=DEFAULT_GAS,
    unsigned=False,
    sequence=None,
    extra_args="",
):
    try:
        if unsigned:
            command = f"{DAEMON} tx staking unbond {validator_addr} {amount}{DENOM} --from {from_key} --chain-id {CHAINID} --output json --node {RPC} --gas {gas} --generate-only"
            tx, tx_err = exec_command(command)
            if len(tx_err):
                return False, tx_err
            return True, json.loads(tx)
        else:
            if sequence is not None:
                command = f"{DAEMON} tx staking unbond {validator_addr} {amount}{DENOM} --from {from_key} --chain-id {CHAINID} --output json --node {RPC} --gas {gas} --keyring-backend test --home {DAEMON_HOME}-1 -y --sequence {sequence}"

            else:
                command = f"{DAEMON} tx staking unbond {validator_addr} {amount}{DENOM} --from {from_key} --chain-id {CHAINID} --output json --node {RPC} --gas {gas} --keyring-backend test --home {DAEMON_HOME}-1 -y"
            tx, tx_err = exec_command(command)
            tx = json.loads(tx)
            if len(tx_err):
                return False, tx_err
            elif tx["code"] != 0:
                return False, tx
            return True, tx
    except Exception as e:
        return False, e


# tx_create_validator takes from key, amount moniker and noded ir as params and
# internally calls `create-validator` to create a new validator initialized with a self-delegation to it and returns json response.
def tx_create_validator(
    from_key,
    amount,
    moniker,
    node_dir,
    gas=DEFAULT_GAS,
    sequence=None,
    extra_args="",
):
    try:
        public_key, err = fetch_validator_pubkey_from_node(node_dir)
        if err:
            return False, err

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
