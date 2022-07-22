from utils import exec_command, env

DAEMON = env.DAEMON
RPC = env.RPC
CHAINID = env.CHAINID


def query_params():
    command = (
        f"{DAEMON} q slashing params --node {RPC} --chain-id {CHAINID} --output json"
    )
    return exec_command(command)


def query_signing_info(consensus_pubkey):
    command = f"{DAEMON} q slashing signing-info {consensus_pubkey} --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)


def query_signing_infos():
    command = f"{DAEMON} q slashing signing-infos --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)
