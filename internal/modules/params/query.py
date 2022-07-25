"""
This module queries params sub commands.
"""
from utils import exec_command, env


DAEMON = env.DAEMON
RPC = env.RPC
CHAINID = env.CHAINID

# `query_subspace` queries params of individual modules
# associated with subspace and key
def query_subspace(subspace, key):
    command = f"""{DAEMON} q params subspace {subspace} {key} --node {RPC} \
        --chain-id {CHAINID} --output json"""
    return exec_command(command)
