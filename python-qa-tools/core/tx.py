import logging
import os, json

from utils import exec_command
from stats import TX_TYPE

CHAINID = os.getenv("CHAINID")
DAEMON = os.getenv("DAEMON")
DAEMON_HOME = os.getenv("DAEMON_HOME")
HOME = os.getenv("HOME")
RPC = os.getenv("RPC")

# The function `tx_sign` will call cosmos-sdk command `tx sign` and the returns the response in json format.
def tx_sign(unsigned_file_name, from_address, sequence, gas="auto", test_type=None):
    try:
        command = f"{DAEMON} tx sign {HOME}/{unsigned_file_name} --from {from_address} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --signature-only=false --sequence {sequence} --gas {gas} --output json"
        signTx, signTxerr = exec_command(command, test_type, TX_TYPE)
        if len(signTxerr):
            return False, signTxerr
        return True, json.loads(signTx)
    except Exception as e:
        return False, e


# The function `tx_broadcast` will call cosmos-sdk command `tx broadcast` and the returns the response in json format.
def tx_broadcast(signed_file, gas, broadcast_mode="sync", test_type=None):
    try:
        if broadcast_mode == "block":
            logging.info("Waiting for transaction for being broadcasted")
        command = f"{DAEMON} tx broadcast {HOME}/{signed_file} --output json --chain-id {CHAINID} --gas {gas} --node {RPC} --broadcast-mode {broadcast_mode}"
        broadcastTx, broadcasterr = exec_command(command, test_type, TX_TYPE)
        broadcastTx = json.loads(broadcastTx)
        if len(broadcasterr):
            return False, broadcasterr
        elif broadcastTx["code"] != 0:
            return False, broadcastTx
        return True, broadcastTx
    except Exception as e:
        return False, e
