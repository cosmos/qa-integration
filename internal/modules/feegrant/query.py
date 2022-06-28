import os, json
from utils import exec_command

DAEMON = os.getenv("DAEMON")
RPC = os.getenv("RPC")
CHAINID = os.getenv("CHAINID")

# `query_feegrant_grant` query details of a single grant.
def query_feegrant_grant(granter, grantee):
    try:
        command = f"{DAEMON} q feegrant grant {granter} {grantee} --node {RPC} --chain-id {CHAINID} --output json"
        grant, err = exec_command(command)
        if len(err):
            return False, err
        return True, json.loads(grant)
    except Exception as e:
        return False, e

# `query_feegrant_grants` query all grants of a grantee.
def query_feegrant_grants(grantee):
    try:
        command = f"{DAEMON} q feegrant grants {grantee} --node {RPC} --chain-id {CHAINID} --output json"
        grant, err = exec_command(command)
        if len(err):
            return False, err
        return True, json.loads(grant)
    except Exception as e:
        return False, e