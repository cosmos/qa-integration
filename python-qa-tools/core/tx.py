"""
This module contains functions calling the `tx` commands.
"""
import logging
import os
import json
from utils import exec_command

CHAINID = os.getenv('CHAINID')
DAEMON = os.getenv('DAEMON')
DAEMON_HOME = os.getenv('DAEMON_HOME')
HOME = os.getenv('HOME')
RPC = os.getenv('RPC')

def tx_sign(unsigned_file_name, from_address, sequence, gas="auto"):
    """
    The function `tx_sign` will call cosmos-sdk command `tx sign`
    and the returns the response in json format.
    """
    try:
        command = f'''{DAEMON} tx sign {HOME}/{unsigned_file_name} --from {from_address}
        --chain-id {CHAINID} --keyring-backend test
        --home {DAEMON_HOME}-1 --node {RPC} --signature-only=false 
        --sequence {sequence} --gas {gas} --output json'''
        sign_tx, sign_tx_err = exec_command(command)
        if len(sign_tx_err) != 0:
            return False, sign_tx_err
        return True, json.loads(sign_tx)
    except Exception as error: # pylint: disable=broad-except
        return False, error

def tx_broadcast(signed_file, gas, broadcast_mode="sync"):
    """
    The function `tx_broadcast` will call cosmos-sdk command `tx broadcast`
    and the returns the response in json format.
    """
    try:
        if broadcast_mode == "block":
            logging.info('Waiting for transaction for being broadcasted')
        command = f'''{DAEMON} tx broadcast {HOME}/{signed_file} --output json
        --chain-id {CHAINID} --gas {gas} --node {RPC} --broadcast-mode {broadcast_mode}'''
        broadcast_tx, broadcast_err = exec_command(command)
        broadcast_tx = json.loads(broadcast_tx)
        if len(broadcast_err) != 0:
            return False, broadcast_err
        if broadcast_tx['code'] != 0:
            return False, broadcast_tx
        return True, broadcast_tx
    except Exception as error: # pylint: disable=broad-except
        return False, error
