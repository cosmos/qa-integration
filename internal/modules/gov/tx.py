import os
from utils import exec_command, env

DAEMON = env.DAEMON
DAEMON_HOME = env.DAEMON_HOME
RPC = env.RPC
CHAINID = env.CHAINID
DEFAULT_GAS = env.DEFAULT_GAS

# tx_submit_proposal internally calls the submit proposal transaction with given proposal type
# and return the response in json format.
def tx_submit_proposal(
    from_key,
    proposal_file_or_name,
    proposal_type="software-upgrade",
    gas=DEFAULT_GAS,
    extra_args="",
):
    command = f"""{DAEMON} tx gov submit-proposal {proposal_type} {proposal_file_or_name} --chain-id {CHAINID} --keyring-backend test \
 --home {DAEMON_HOME}-1 --from {from_key} --node {RPC} --output json -y --gas {gas}"""
    return exec_command(command, extra_args)


# tx_cancel_software_upgrade internally calls the cancel software upgrade tx command
# and return the response in json format.
def tx_cancel_software_upgrade(
    from_key,
    gas=DEFAULT_GAS,
    extra_args="",
):
    command = f"""{DAEMON} tx gov submit-proposal cancel-software-upgrade --chain-id {CHAINID} --keyring-backend test \
 --home {DAEMON_HOME}-1 --from {from_key} --node {RPC} --output json -y --gas {gas}"""
    return exec_command(command, extra_args)


# tx_deposit internally calls the 'gov deposit' tx command and return the response in json format
def tx_deposit(
    from_key,
    proposal_id,
    deposit,
    gas=DEFAULT_GAS,
    extra_args="",
):
    command = f"""{DAEMON} tx gov deposit {proposal_id} {deposit} --chain-id {CHAINID} --keyring-backend test \
 --home {DAEMON_HOME}-1 --from {from_key} --node {RPC} --output json -y --gas {gas}"""
    return exec_command(command, extra_args)


# tx_vote internally calls the 'gov vote' tx command and return the response in json format
def tx_vote(
    from_key,
    proposal_id,
    option,
    gas=DEFAULT_GAS,
    home=f"{DAEMON_HOME}-1",
    extra_args="",
):
    command = f"""{DAEMON} tx gov vote {proposal_id} {option} --chain-id {CHAINID} --keyring-backend test \
 --home {home} --from {from_key} --node {RPC} --output json -y --gas {gas}"""
    return exec_command(command, extra_args)


# tx_weighted_vote internally calls the 'gov weighted_vote' tx command and return the response in json format
def tx_weighted_vote(
    from_key,
    proposal_id,
    options,
    gas=DEFAULT_GAS,
    home=f"{DAEMON_HOME}-1",
    extra_args="",
):
    command = f"""{DAEMON} tx gov weighted-vote {proposal_id} {options} --chain-id {CHAINID} --keyring-backend test \
 --home {home} --from {from_key} --node {RPC} --output json -y --gas {gas}"""
    return exec_command(command, extra_args)
