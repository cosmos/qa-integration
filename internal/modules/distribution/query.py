"""
This module consists of query commands for distribution module
"""
from utils import exec_command, env

DAEMON = env.DAEMON
RPC = env.RPC
CHAINID = env.CHAINID


def query_commission_rewards(validator_addr):
    """`query_commissio_rewards` fetches validator
    commission rewards and return response in json formate"""

    command = f"{DAEMON} q distribution commission {validator_addr} \
        --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)


def query_community_pool():
    """`query_community_pool` fetches community pool fund and
    return response in json formate
    """

    command = f"{DAEMON} q distribution community-pool --node {RPC} \
    --chain-id {CHAINID} --output json"
    return exec_command(command)


def query_params():
    """`query_params` fetches distribution module params and
    returns response in json formate
    """

    command = f"{DAEMON} q distribution params --node {RPC} \
    --chain-id {CHAINID} --output json"
    return exec_command(command)


def query_rewards_singleval(delegator_addr, validator_addr):
    """`query_rewards_singleval` fetches given validator rewards and
    returns response in json format
    """

    command = f"{DAEMON} q distribution rewards {delegator_addr} {validator_addr} \
    --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)


def query_rewards(delegator_addr):
    """query_rewards fetches given delegator rewards and
    returns response in json formate
    """

    command = f"{DAEMON} q distribution rewards {delegator_addr} --node {RPC} \
        --chain-id {CHAINID} --output json"
    return exec_command(command)


def query_slashes(validator_addr, start_height, end_height):
    """`query_slashes` fetches validator's slashes info and
    returns response in json formate
    """

    command = f"{DAEMON} q distribution slashes {validator_addr} {start_height} {end_height} \
        --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)


def query_validator_outstanding_rewards(validator_addr):
    """`query_validator_outstanding_rewards` fetches validator's outstanding rewards
    and returns response in json formate
    """
    command = f"{DAEMON} q distribution validator-outstanding-rewards {validator_addr} \
        --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)
