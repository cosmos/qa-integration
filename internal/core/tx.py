"""
This module contains functions calling the `tx` commands.
"""
import logging
import os
from internal.utils import exec_command

CHAINID = os.getenv("CHAINID")
DAEMON = os.getenv("DAEMON")
DAEMON_HOME = os.getenv("DAEMON_HOME")
HOME = os.getenv("HOME")
RPC = os.getenv("RPC")


def tx_sign(unsigned_file_name, from_address, sequence, gas="auto"):
    """The function `tx_sign` will call cosmos-sdk command `tx sign`
        and the returns the response in json format.

    Args:
        unsigned_file_name (_str_): file path to store unsigned transactions.
        from_address (_str_): Name or address of private key with which to sign.
        sequence (_uint_): The sequence number of the signing account (offline mode only)
        gas (str, optional): gas limit to set per-transaction;
        set to "auto" to calculate sufficient gas automatically (default 200000).

    Returns:
        _tuple_: (boolean, json|str)
    """
    command = f"""{DAEMON} tx sign {HOME}/{unsigned_file_name} --from {from_address} \
--chain-id {CHAINID} --keyring-backend test \
--home {DAEMON_HOME}-1 --node {RPC} --signature-only=false \
--sequence {sequence} --gas {gas} --output json"""
    return exec_command(command)


def tx_broadcast(signed_file, gas, broadcast_mode="sync"):
    """
    Broadcast transactions created with the --generate-only
    flag and signed with the sign command. Read a transaction from [file_path] and
    broadcast it to a node.

    Args:
        signed_file (_str_): file path to store signed transactions.
        gas (_int_): gas limit to set per-transaction; set to "auto"
        to calculate sufficient gas automatically (default 200000)
        broadcast_mode (str, optional): Transaction broadcasting mode (sync|async|block)
        (default "sync").

    Returns:
        _tuple_: (boolean, json|str)
    """

    if broadcast_mode == "block":
        logging.info("Waiting for transaction for being broadcasted")
    command = f"""{DAEMON} tx broadcast {HOME}/{signed_file} --output json \
--chain-id {CHAINID} --gas {gas} --node {RPC} --broadcast-mode {broadcast_mode}"""
    return exec_command(command)
