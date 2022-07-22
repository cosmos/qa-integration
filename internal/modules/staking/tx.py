import json
from utils import exec_command, env
from modules.staking.query import (
    fetch_validator_pubkey_from_node,
)

DAEMON = env.DAEMON
DENOM = env.DENOM
CHAINID = env.CHAINID
HOME = env.HOME
DAEMON_HOME = env.DAEMON_HOME
RPC = env.RPC
DEFAULT_GAS = env.DEFAULT_GAS

# tx_delegate takes from_key, validator address and amount as paramaters and
# internally executes the 'delegate tx' command and return the response in json format.
def tx_delegate(from_key, validator_addr, amount, gas=DEFAULT_GAS):
    command = f"{DAEMON} tx staking delegate {validator_addr} {amount}{DENOM} --from {from_key} --chain-id {CHAINID} --output json --node {RPC} --gas {gas} --keyring-backend test --home {DAEMON_HOME}-1 -y"
    return exec_command(command)


# tx_redelegate takes from_key, source and disration validator address as params and
# internally executes the 'redelegate tx' command and return the response in json format.
def tx_redelegate(
    from_key,
    src_validator_addr,
    dst_validator_addr,
    amount,
    gas=DEFAULT_GAS,
):

    command = f"{DAEMON} tx staking redelegate {src_validator_addr} {dst_validator_addr} {amount}{DENOM} --from {from_key} --chain-id {CHAINID} --output json --node {RPC} --gas {gas} --keyring-backend test --home {DAEMON_HOME}-1 -y"
    return exec_command(command)


# tx_unbond takes from key, valiator address and amount as params and
# internally executes the 'unbond tx' command and return the response in json format.
def tx_unbond(
    from_key,
    validator_addr,
    amount,
    gas=DEFAULT_GAS,
):
    command = f"{DAEMON} tx staking unbond {validator_addr} {amount}{DENOM} --from {from_key} --chain-id {CHAINID} --output json --node {RPC} --gas {gas} --keyring-backend test --home {DAEMON_HOME}-1 -y"
    return exec_command(command)


# tx_create_validator takes from key, amount moniker and noded id as params and
# internally calls `create-validator` to create a new validator initialized with a self-delegation to it and returns json response.
def tx_create_validator(
    from_key,
    amount,
    moniker,
    node_dir,
    gas=DEFAULT_GAS,
):
    status, public_key = fetch_validator_pubkey_from_node(node_dir)
    if not status:
        return False, public_key
    public_key = json.dumps(public_key, separators=(",", ":"))

    command = f"{DAEMON} tx staking create-validator --amount {amount}{DENOM} --commission-max-change-rate 0.1 --commission-max-rate 0.2 --commission-rate 0.1 --from {from_key} --min-self-delegation 1 --moniker {moniker} --pubkey {public_key}  --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --gas {gas}"
    return exec_command(command)


# tx_edit_validator edit an existing validator account.
def tx_edit_validator(
    from_key,
    moniker,
    gas=DEFAULT_GAS,
):
    command = f"{DAEMON} tx staking edit-validator --moniker {moniker} --from {from_key} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --gas {gas}"
    return exec_command(command)
