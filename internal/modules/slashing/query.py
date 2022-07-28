"""
This module consists of query commands for slashing module
"""
from utils import exec_command, env

DAEMON = env.DAEMON
RPC = env.RPC
CHAINID = env.CHAINID


def query_params():
    """`query_params` fetches slashing module params and returns response in json format"""

    command = (
        f"{DAEMON} q slashing params --node {RPC} --chain-id {CHAINID} --output json"
    )
    return exec_command(command)


def query_signing_info(consensus_pubkey):
    """`query_signing_info` fetches given validator's signing information
    and returns response in json format
    """

    command = f"{DAEMON} q slashing signing-info {consensus_pubkey} --node {RPC} \
            --chain-id {CHAINID} --output json"
    return exec_command(command)


def query_signing_infos():
    """`query_signing_infos` fetches signing information of all validators
    and returns response in json format
    """
    command = f"{DAEMON} q slashing signing-infos --node {RPC} \
            --chain-id {CHAINID} --output json"
    return exec_command(command)
