"""
This module consists of query commands for auth cosmos-sdk module
"""
import argparse
import os
from internal.utils import exec_command

DAEMON = os.getenv("DAEMON")
RPC = os.getenv("RPC")


def account_type(address):
    """account type is an user-defined data type used
    to validate account addresses read from Argument Parser.

    Args:
        address (_str_): bech32 address to be queried.

    Raises:
        argparse.ArgumentTypeError: This Error is raised if the bech32 address is not valid.

    Returns:
        _tuple_: (boolean, json|str)
    """
    status, response = query_account(address)
    if not status:
        raise argparse.ArgumentTypeError(response)
    return address


def query_account(address):
    """query account function will take the bech32 address
    as input and output the information of account.

    Args:
        address (_str_): bech32 address to be queried.

    Returns:
        _tuple_: (bool, json|str)
    """
    command = f"{DAEMON} query auth account {address} --node {RPC} --output json"
    return exec_command(command)
