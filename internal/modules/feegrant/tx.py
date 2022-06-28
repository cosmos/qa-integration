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
    unsigned=False,
    sequence=None,
):
    try:
        command = f"{DAEMON} tx feegrant grant {granter_key} {grantee} --spend-limit 100stake --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --gas {gas}"
        print(f"comandddddd.......{command}")
        Tx, Txerr = exec_command(command)
        Tx = json.loads(Tx)
        if len(Txerr):
            return False, Txerr
        elif Tx["code"] != 0:
            return False, Tx
        return True, Tx
    except Exception as e:
        return False, e
