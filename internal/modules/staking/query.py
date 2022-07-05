"""
This module queries staking sub commands.
"""
import os
from internal.utils import exec_command

DAEMON = os.getenv("DAEMON")
RPC = os.getenv("RPC")
CHAINID = os.getenv("CHAINID")


def query_staking_validators():
    """
    The function 'query_staking_validators' fetches the validators information.
    Returns:
        _tuple_: (bool, str|json)
    """
    command = (
        f"{DAEMON} q staking validators --node {RPC} --chain-id {CHAINID} --output json"
    )
    return exec_command(command)


def query_staking_delegations(delegator, validator):
    """
    The function `query_staking_delegations` fetches the information
    about the delagator delegations for a validator.
    Args:
        delegator (_str_): delegator bech32 address
        validator (_str_): validator bech32 address

    Returns:
        _tuple_: (bool, str|json)
    """

    command = f"""{DAEMON} q staking delegation {delegator} {validator} \
--node {RPC} --chain-id {CHAINID} --output json"""
    return exec_command(command)
