"""
Querying functions for the bank module.
"""
import os
import json

from utils import exec_command

DAEMON = os.getenv('DAEMON')
RPC = os.getenv('RPC')


def query_balances(address):
    """
    query_balances returns the balance json by taking bech32 address as parameter.
    Args:
        address (_str_): bech32 address

    Returns:
        _tuple_: (boolean,str|json)
    """
    try:
        command = f"{DAEMON} q bank balances {address} --node {RPC} --output json"
        balance, balance_err = exec_command(command)
        if len(balance_err) != 0:
            return False, balance_err
        return True, json.loads(balance)
    except Exception as error:  # pylint: disable=broad-except
        return False, error
