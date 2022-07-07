import json, os
from utils import exec_command

DAEMON = os.getenv("DAEMON")
DENOM = os.getenv("DENOM")
CHAINID = os.getenv("CHAINID")
HOME = os.getenv("HOME")
DAEMON_HOME = os.getenv("DAEMON_HOME")
RPC = os.getenv("RPC")
DEFAULT_GAS = 2000000

# `tx_grant` takes granter_key and grantee address as paramaters and executes feegrant grant tx
# internally and returns the json response.
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

# `set_periodic_expiration_grant` takes granter_key and grantee address as paramaters and executes grant tx
# internally and returns the json response.
def set_periodic_expiration_grant(
    granter_key,
    grantee,
    gas=DEFAULT_GAS,
):
    try:
        command = f"{DAEMON} tx feegrant grant {granter_key} {grantee} --spend-limit 100stake --period 60 --period-limit 10stake --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --gas {gas}"
        Tx, tx_err = exec_command(command)
        Tx = json.loads(Tx)
        if len(tx_err):
            return False, tx_err
        elif Tx["code"] != 0:
            return False, Tx
        return True, Tx
    except Exception as e:
        return False, e

# `tx_revoke_feegrant` takes granter_key and grantee address as paramaters and executes feegrant revoke tx
# internally and returns the json response.
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