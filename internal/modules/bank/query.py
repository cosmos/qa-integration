"""
Querying functions for the bank module.
"""
import sys

from internal.utils import exec_command, print_balance_deductions, env

DAEMON = env.DAEMON
RPC = env.RPC
DENOM = env.DENOM


def query_balances(address):
    """
    query_balances returns the balance json by taking bech32 address as parameter.
    Args:
        address (_str_): bech32 address

    Returns:
        _tuple_: (boolean,str|json)
    """
    command = f"{DAEMON} q bank balances {address} --node {RPC} --output json"
    return exec_command(command)


def calculate_balance_deductions(
    sender, receiver, sender_balance_old, receiver_balance_old  # pylint: disable=c0330
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


def query_total_suuply():
    command = f"{DAEMON} q bank total --denom={DENOM} --node {RPC} --output json"
    return exec_command(command)
