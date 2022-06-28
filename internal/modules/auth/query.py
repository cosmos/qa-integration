"""
This module consists of query commands for auth cosmos-sdk module
"""
import argparse
import os
import sys
from internal.utils import process_response

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
    return process_response(command)


def get_sequences(sender, receiver):
    """
    This function returns sequence numbers for sender and receiver.
    Args:
        sender (_str_): Sender Bech32 address.
        receiver (_str_):Receiver Bech32 address.

    Returns:
        _tuple_: int, int
    """
    status, sender_acc = query_account(sender)
    if not status:
        sys.exit(sender_acc)

    status, receiver_acc = query_account(receiver)
    if not status:
        sys.exit(receiver_acc)

    sender_acc_seq, receiver_acc_seq = int(sender_acc["sequence"]), int(
        receiver_acc["sequence"]
    )
    return sender_acc_seq, receiver_acc_seq
