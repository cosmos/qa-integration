import json, os
from utils import exec_command

DAEMON = os.getenv("DAEMON")
DENOM = os.getenv("DENOM")
CHAINID = os.getenv("CHAINID")
HOME = os.getenv("HOME")
DAEMON_HOME = os.getenv("DAEMON_HOME")
RPC = os.getenv("RPC")
DEFAULT_GAS = 2000000

# tx_grant grant authorization to pay fees from your address.
def tx_grant(
    granter_key,
    grantee,
    gas=DEFAULT_GAS,
):
    try:
        command = f"{DAEMON} tx feegrant grant {granter_key} {grantee} --spend-limit 100stake --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --gas {gas}"
        Tx, tx_err = exec_command(command)
        Tx = json.loads(Tx)
        if len(tx_err):
            return False, tx_err
        elif Tx["code"] != 0:
            return False, Tx
        return True, Tx
    except Exception as e:
        return False, e

# set_periodic_expiration_grant sents periodic expirtaion for grant transaction.
def set_periodic_expiration_grant(
    granter_key,
    grantee,
    gas=DEFAULT_GAS,
):
    try:
        command = f"{DAEMON} tx feegrant grant {granter_key} {grantee} --spend-limit 100stake --period 3600 --period-limit 10stake --expiration 36000 --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --gas {gas}"
        Tx, tx_err = exec_command(command)
        Tx = json.loads(Tx)
        if len(tx_err):
            return False, tx_err
        elif Tx["code"] != 0:
            return False, Tx
        return True, Tx
    except Exception as e:
        return False, e

# tx_revoke revoke fee grant from a granter to a grantee.
def tx_revoke_feegrant(
    granter_key,
    grantee,
    gas=DEFAULT_GAS,
):
    try:
        command = f"{DAEMON} tx feegrant revoke {granter_key} {grantee} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --gas {gas}"
        Tx, tx_err = exec_command(command)
        Tx = json.loads(Tx)
        if len(tx_err):
            return False, tx_err
        elif Tx["code"] != 0:
            return False, Tx
        return True, Tx
    except Exception as e:
        return False, e