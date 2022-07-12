import os
from utils import exec_command

DAEMON = os.getenv("DAEMON")
RPC = os.getenv("RPC")
CHAINID = os.getenv("CHAINID")

# `query_authz_grants` queries grants for a granter-grantee pair and returns the json response.
def query_authz_grants(granter, grantee):
        command = f"{DAEMON} q authz grants {granter} {grantee} --node {RPC} --chain-id {CHAINID} --output json --count-total"
        return exec_command(command)

# `query_authz_grantee_grants` queries authorization grants granted to a grantee and returns json response.
def query_authz_grantee_grants(grantee):
        command = f"{DAEMON} q authz grantee-grants {grantee} --node {RPC} --chain-id {CHAINID} --output json"
        return exec_command(command)


# `query_authz_granter_grants` queries authorization grants granted by granter and returns json response.
def query_authz_granter_grants(granter):
        command = f"{DAEMON} q authz granter-grants {granter} --node {RPC} --chain-id {CHAINID} --output json"
        return exec_command(command)
