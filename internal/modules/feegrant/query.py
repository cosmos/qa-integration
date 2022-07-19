from utils import exec_command, env

DAEMON = env.DAEMON
RPC = env.RPC
CHAINID = env.CHAINID

# `query_feegrant_grant` takes grannter and grantee addresses as pramaters and returns json response.
def query_feegrant_grant(granter, grantee):
    command = f"{DAEMON} q feegrant grant {granter} {grantee} --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)


# `query_greantee_grants` takes grantee address as paramter and returns the grants of grantee in json response.
def query_greantee_grants(grantee):
    command = f"{DAEMON} q feegrant grants {grantee} --node {RPC} --chain-id {CHAINID} --output json --count-total"
    return exec_command(command)
