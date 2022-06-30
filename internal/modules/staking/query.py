"""
This module queries staking sub commands.
"""
import os
import json
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
    try:
        command = f"{DAEMON} q staking validators --node {RPC} --chain-id {CHAINID} --output json"
        validators, validatorserr = exec_command(command)
        print(f"staking validators command: {command}")
        if len(validatorserr) != 0:
            return False, validatorserr
        return True, json.loads(validators)
    except Exception as error:  # pylint: disable=broad-except
        return False, error


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
    try:
        command = f"""{DAEMON} q staking delegation {delegator} {validator} \
--node {RPC} --chain-id {CHAINID} --output json"""
        print(f"staking delegation command: {command}")
        delegations, delegationerr = exec_command(command)
        if len(delegationerr) != 0:
            return False, delegationerr
        return True, json.loads(delegations)
    except Exception as error:  # pylint: disable=broad-except
        return False, error
