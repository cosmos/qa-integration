"""
This module contains all util functions.
"""
import argparse
import os
import json
import logging
import subprocess
from shutil import which

logging.basicConfig(format='%(message)s',
                    level=logging.DEBUG)

DAEMON = os.getenv('DAEMON')
HOME = os.getenv('HOME')


def print_balance_deductions(wallet, diff):
    """
    The function `print_balance_deductions` will print information about the
    balance deductions after transactions for a wallet or account.
    Args:
        wallet (_str_): wallet name
        diff (_uint_): balance difference.
    """
    if diff > 0:
        logging.error('Some of the transactions failed')
        logging.info('Balance in the %s increased by %s', wallet, diff)
    elif diff < 0:
        logging.error('Some of the transactions failed')
        logging.info('Balance in the %s decreased by %s', wallet, (-1 * diff))
    else:
        logging.info(
            'All transaction went successfully, No deduction from %s balance', wallet)


def exec_command(command):
    """
    The utility function `exec_command` is used to execute the cosmos-sdk based commands.
    Args:
        command (_str_): Command to be executed.

    Returns:
        _tuple_: str, str
    """
    stdout, stderr = subprocess.Popen(command.split(),
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE).communicate()
    return stdout.strip().decode(), stderr.strip().decode()


def is_tool(binary):
    """
    The utility function `is_tool` is used to verify the package or binary installation.
    """
    return which(binary) is not None


def num_txs_type(num_x):
    """
    num_txs_type is a user-defined type.
    Args:
        num_x (_unit_): int

    Raises:
        argparse.ArgumentTypeError

    Returns:
        _int_: int
    """
    if int(num_x) < 1000:
        raise argparse.ArgumentTypeError(
            'The argument NUM_TXS should be 1000 or more')
    return int(num_x)


def node_type(num_x):
    """
    node_type is a user-defined type.
    Args:
        num_x (_int_): int

    Raises:
        argparse.ArgumentTypeError

    Returns:
        _int_: _int_
    """
    num_x = int(num_x)
    if num_x < 2:
        raise argparse.ArgumentTypeError(
            f"The number of nodes should be atleast 2, you have entered {num_x}")
    return num_x


def create_multi_messages(num_msgs, file_name):
    """
    The function `create_multi_messages` is used to duplicate the messages in a single transaction.
    Args:
        num_msgs (_uint_): uint
        file_name (_str_): file path to modify messages.
    """
    messages = []
    with open(f"{HOME}/{file_name}", 'r+') as file:
        file_data = json.load(file)
        messages.append(file_data["body"]["messages"][-1])
    for _i in range(num_msgs):
        messages.append(messages[-1])

    with open(f"{HOME}/{file_name}", 'r+') as file:
        file_data = json.load(file)
        file_data["body"]["messages"] = messages
        file.seek(0)
        json.dump(file_data, file, indent=4)
