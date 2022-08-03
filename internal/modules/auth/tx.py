"""This module covers the tx commands of auth CosmosSDK module"""
from datetime import datetime, timedelta
from internal.utils import exec_command, env

DAEMON = env.DAEMON
HOME = env.HOME
DENOM = env.DENOM
CHAIN_ID = env.CHAINID
DAEMON_HOME = env.DAEMON_HOME
RPC = env.RPC


def tx_encode(signed_file: str):
    """This function encodes a unsigned transaction file"""
    command = f"{DAEMON} tx encode {HOME}/{signed_file}"
    return exec_command(command)


def tx_decode(encoded_tx):
    """This function decodes an encoded transaction"""
    return exec_command(f"{DAEMON} tx decode {encoded_tx}")


def tx_create_vesting_account(
    address: str,
    amount: int,
    from_account: str = "account1",
    home: str = f"{DAEMON_HOME}-1",
    end_time: str = (datetime.now() + timedelta(minutes=1)).strftime("%s"),
    delayed: bool = False,
):
    command = f"{DAEMON} tx vesting create-vesting-account {address} \
{amount}{DENOM} {end_time} --from {from_account} --home {home} \
--keyring-backend test --node {RPC} --chain-id {CHAIN_ID} --output json -y"
    if delayed:
        command = command + " --delayed"
    return exec_command(command)
