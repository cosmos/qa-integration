import json, os
from utils import exec_command
from modules.bank.tx import (
    tx_send,
)

DAEMON = os.getenv("DAEMON")
DENOM = os.getenv("DENOM")
CHAINID = os.getenv("CHAINID")
HOME = os.getenv("HOME")
DAEMON_HOME = os.getenv("DAEMON_HOME")
RPC = os.getenv("RPC")
DEFAULT_GAS = 2000000

# `execute_authz_tx` takes the granter_key and tx_file as parameters and executes the authz exec tx
# internally and returns the json.
def execute_authz_tx(
    grantee_key,
    tx_file,
    gas=DEFAULT_GAS,
):
    try:
        command = f"{DAEMON} tx authz exec {tx_file} --from {grantee_key} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --gas {gas}"
        tx, tx_err = exec_command(command)
        tx = json.loads(tx)
        if len(tx_err):
            return False, tx_err
        elif tx["code"] != 0:
            return False, tx
        return True, tx
    except Exception as e:
        return False, e


# `tx_grant_authz` takes the granter and grantee as parameters and executes the authz grant tx
# internally and returns the json.
def tx_grant_authz(
    granter,
    grantee,
    gas=DEFAULT_GAS,
):
    try:
        command = f"{DAEMON} tx authz grant {grantee} send --spend-limit 100stake --from {granter} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --gas {gas}"
        tx, tx_err = exec_command(command)
        tx = json.loads(tx)
        if len(tx_err):
            return False, tx_err
        elif tx["code"] != 0:
            return False, tx
        return True, tx
    except Exception as e:
        return False, e


# `tx_revoke_authz` takes the granter and grantee as parameters and executes the authz revoke tx
# internally and returns the json.
def tx_revoke_authz(
    granter,
    grantee,
    gas=DEFAULT_GAS,
):
    try:
        command = f"{DAEMON} tx authz revoke {grantee} /cosmos.bank.v1beta1.MsgSend --from {granter} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --gas {gas}"
        tx, tx_err = exec_command(command)
        tx = json.loads(tx)
        if len(tx_err):
            return False, tx_err
        elif tx["code"] != 0:
            return False, tx
        return True, tx
    except Exception as e:
        return False, e


# The function 'create_unsigned_send_tx' takes sender(from_address), receiver(to_address), amount and file_name as parameters and call the function tx_send
# internally and stores the json to file_name file.
def create_unsigned_send_tx(from_address, to_address, amount, file_name):
    try:
        status, unsignedTx = tx_send(
            from_address,
            to_address,
            amount,
            gas=DEFAULT_GAS,
            unsigned=True,
        )
        if not status:
            return status, unsignedTx
        with open(f"{file_name}", "w") as outfile:
            json.dump(unsignedTx, outfile)
        return True, unsignedTx
    except Exception as e:
        return False, e
