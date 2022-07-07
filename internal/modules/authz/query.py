import os, json
from utils import exec_command

DAEMON = os.getenv("DAEMON")
RPC = os.getenv("RPC")
CHAINID = os.getenv("CHAINID")

# `query_authz_grants` takes granter and grantee as paramaters, queries the authz grants
# internally and returns the json response.
def query_authz_grants(granter, grantee):
    try:
        command = f"{DAEMON} q authz grants {granter} {grantee} --node {RPC} --chain-id {CHAINID} --output json"
        grant, err = exec_command(command)
        if len(err):
            return False, err
        return True, json.loads(grant)
    except Exception as e:
        return False, e


# `query_authz_grantee_grants` takes grantee address as paramater and calls authz grantee-grants
# internally and returns the json response.
def query_authz_grantee_grants(grantee):
    try:
        command = f"{DAEMON} q authz grantee-grants {grantee} --node {RPC} --chain-id {CHAINID} --output json"
        grant, err = exec_command(command)
        if len(err):
            return False, err
        return True, json.loads(grant)
    except Exception as e:
        return False, e


# `query_authz_granter_grants` takes granter address as paramater and calls authz granter-grants
# internally and returns the json response.
def query_authz_granter_grants(granter):
    try:
        command = f"{DAEMON} q authz granter-grants {granter} --node {RPC} --chain-id {CHAINID} --output json"
        grant, err = exec_command(command)
        if len(err):
            return False, err
        return True, json.loads(grant)
    except Exception as e:
        return False, e
