"""
This module consists of tx commands for slashing module
"""
from utils import exec_command, env

DAEMON = env.DAEMON
DENOM = env.DAEMON
CHAINID = env.CHAINID
HOME = env.HOME
DAEMON_HOME = env.DAEMON_HOME
RPC = env.RPC
DEFAULT_GAS = env.DEFAULT_GAS


def tx_unjail(
    from_key,
    gas=DEFAULT_GAS,
):

    """`tx_unjail` unjail validator previously jailed for downtime."""

    command = f"{DAEMON} tx slashing unjail --from {from_key} --chain-id {CHAINID} \
        --keyring-backend test --home {DAEMON_HOME}-3 --node {RPC} --output json -y --gas {gas}"
    return exec_command(command)
