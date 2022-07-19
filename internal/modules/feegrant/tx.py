from utils import exec_command, env

DAEMON = env.DAEMON
DENOM = env.DENOM
CHAINID = env.CHAINID
HOME = env.HOME
DAEMON_HOME = env.DAEMON_HOME
RPC = env.RPC
DEFAULT_GAS = env.DEFAULT_GAS

# `tx_grant` takes granter_key and grantee address as paramaters and executes feegrant grant tx
# internally and returns the json response.
def tx_grant(
    granter_key,
    grantee,
    gas=DEFAULT_GAS,
):
    command = f"{DAEMON} tx feegrant grant {granter_key} {grantee} --spend-limit 100stake --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --gas {gas}"
    return exec_command(command)


# `set_periodic_expiration_grant` takes granter_key and grantee address as paramaters and executes grant tx
# internally and returns the json response.
def set_periodic_expiration_grant(
    granter_key,
    grantee,
    gas=DEFAULT_GAS,
):
    command = f"{DAEMON} tx feegrant grant {granter_key} {grantee} --spend-limit 100stake --period 60 --period-limit 10stake --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --gas {gas}"
    return exec_command(command)


# `tx_revoke_feegrant` takes granter_key and grantee address as paramaters and executes feegrant revoke tx
# internally and returns the json response.
def tx_revoke_feegrant(
    granter_key,
    grantee,
    gas=DEFAULT_GAS,
):
    command = f"{DAEMON} tx feegrant revoke {granter_key} {grantee} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --gas {gas}"
    return exec_command(command)
