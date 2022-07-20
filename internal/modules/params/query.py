from utils import exec_command, env


DAEMON = env.DAEMON
RPC = env.RPC
CHAINID = env.CHAINID


def query_subspace(subspace, key):
    command = f"{DAEMON} q params subspace {subspace} {key} --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)
