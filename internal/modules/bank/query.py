"""
Querying functions for the bank module.
"""
import os
import json
import sys

from internal.utils import exec_command, print_balance_deductions

DAEMON = os.getenv("DAEMON")
RPC = os.getenv("RPC")


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


def calculate_balance_deductions(
    sender, receiver, sender_balance_old, receiver_balance_old  # pylint: disable=C0330
):
    """_summary_

    Args:
        sender (_str_): bech32 address.
        receiver (_str_): bech32 address.
        sender_balance_old (_int_): _int_
        receiver_balance_old (_int_): _int_
    """
    status, sender_balance_updated = query_balances(sender)
    if not status:
        sys.exit(sender_balance_updated)
    sender_balance_updated = sender_balance_updated["balances"][0]["amount"]

    status, receiver_balance_updated = query_balances(receiver)
    if not status:
        sys.exit(receiver_balance_updated)
    receiver_balance_updated = receiver_balance_updated["balances"][0]["amount"]

    sender_diff = int(sender_balance_old) - int(sender_balance_updated)
    receiver_diff = int(receiver_balance_old) - int(receiver_balance_updated)

    print_balance_deductions("sender", sender_diff)
    print_balance_deductions("receiver", receiver_diff)
