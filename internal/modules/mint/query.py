"""
This module consists of query commands for mint module
"""
from utils import exec_command, env

DAEMON = env.DAEMON
RPC = env.RPC
CHAINID = env.CHAINID


def query_annual_provision():
    """`query_annual_provision` fetches current minting annual provision value
    and returns response in json formate"""

    command = f"{DAEMON} q mint annual-provisions --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)


def query_inflation():
    """`query_inflation` fetches current minting inflation value and
    returns response in json formate"""

    command = (
        f"{DAEMON} q mint inflation --node {RPC} --chain-id {CHAINID} --output json"
    )
    return exec_command(command)


def query_params():
    """`query_params` fetches mint module params returns response in json format"""

    command = f"{DAEMON} q mint params --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)
