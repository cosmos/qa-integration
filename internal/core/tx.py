"""
This module contains functions calling the `tx` commands.
"""
import logging
from internal.utils import exec_command, env

CHAINID = env.CHAINID
DAEMON = env.DAEMON
DAEMON_HOME = env.DAEMON_HOME
HOME = env.HOME
RPC = env.RPC
DEFAULT_GAS = env.DEFAULT_GAS


def tx_sign(
    unsigned_file_name: str, from_address: str, sequence: int = None, gas: str = "auto"
):
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
    if sequence is not None:
        command = f"""{DAEMON} tx sign {HOME}/{unsigned_file_name} --from {from_address} \
--chain-id {CHAINID} --keyring-backend test \
--home {DAEMON_HOME}-1 --node {RPC} --signature-only=false \
--sequence {sequence} --gas {gas} --output json"""
    else:
        command = f"""{DAEMON} tx sign {HOME}/{unsigned_file_name} --from {from_address} \
--chain-id {CHAINID} --keyring-backend test \
--home {DAEMON_HOME}-1 --node {RPC} --signature-only=false \
--gas {gas} --output json"""

    return exec_command(command)


def tx_partner_sign(
    unsigned_file: str,
    multisig_address: str,
    signer: str,
    home: str = f"{DAEMON_HOME}-1",
    broadcast_mode: str = "sync",
    batch: bool = False,
):
    """
    The function `tx_multi_sign` does the multisig transaction.
    """
    sub_command = "sign-batch" if batch else "sign"
    command = f"""{DAEMON} tx {sub_command} {HOME}/{unsigned_file} --multisig {multisig_address} \
--from {signer} --keyring-backend test --home {home} --chain-id {CHAINID} \
--broadcast-mode {broadcast_mode} --fees {DEFAULT_GAS}stake --node {RPC}"""
    return exec_command(command)


def tx_multi_sign(
    unsigned_file: str,
    multisig_account: str,
    signatures: list,
    home: str = f"{DAEMON_HOME}-1",
    batch: bool = False,
):
    """
    tx_multi_sign
    """
    signs = ""
    for signtaure in signatures:
        signs += f"{HOME}/{signtaure} "
    sub_command = "multisign-batch" if batch else "multisign"
    command = f"""{DAEMON} tx {sub_command} {HOME}/{unsigned_file} {multisig_account} \
{signs} --home {home} --keyring-backend test --chain-id {CHAINID} \
--fees {DEFAULT_GAS}stake --node {RPC}"""
    return exec_command(command)


def tx_broadcast(
    signed_file: str, gas: int = DEFAULT_GAS, broadcast_mode: str = "sync"
):
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
--chain-id {CHAINID} --gas {gas}stake --node {RPC} --broadcast-mode {broadcast_mode}"""
    return exec_command(command)
