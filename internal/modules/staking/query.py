"""
This module queries staking sub commands.
"""
from internal.utils import exec_command, env

DAEMON = env.DAEMON
RPC = env.RPC
CHAINID = env.CHAINID

# 'query_staking_validators' fetches the validators information and return reponse in json format.
def query_staking_validators():
    """
    The function 'query_staking_validators' fetches the validators information.
    Returns:
        _tuple_: (bool, str|json)
    """
    command = (
        f"{DAEMON} q staking validators --node {RPC} --chain-id {CHAINID} --output json"
    )
    return exec_command(command)


# `query_delegator_delegations` queries individual delegator delegations.
def query_delegator_delegations(delegator, validator):
    """
    The function `query_delegator_delegations` fetches the information
    about the delagator delegations for a validator.
    Args:
        delegator (_str_): delegator bech32 address
        validator (_str_): validator bech32 address

    Returns:
        _tuple_: (bool, str|json)
    """

    command = f"""{DAEMON} q staking delegation {delegator} {validator} \
--node {RPC} --chain-id {CHAINID} --output json"""
    return exec_command(command)


# `query_delegator_redelegations` takes delegator address ad params and
# internally calls the `staking redelegations` and returns response of an individual delegator in json format.
def query_delegator_redelegations(delegator_addr):
    command = f"{DAEMON} q staking redelegations {delegator_addr} --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)


# `query_delegator_redelegation` queries single redelegation record for an individual delegator between a source and destination validator.
def query_delegator_redelegation(
    delegator_addr, src_validator_addr, dst_validator_addr
):

    command = f"{DAEMON} q staking redelegation {delegator_addr} {src_validator_addr} {dst_validator_addr} --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)


# `query_unbonding_delegation` queries unbonding delegations for an individual delegator on an individual validator.
def query_unbonding_delegation(delegator_addr, validator_addr):
    command = f"{DAEMON} q staking unbonding-delegation {delegator_addr} {validator_addr} --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)


# `query_validator` queries details about an individual validator and return response in json format.
def query_validator(validator_addr):
    command = f"{DAEMON} q staking validator {validator_addr} --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)


# `query_validator_set` returns details about all validators on a network in the form of json.
def query_validator_set():
    command = (
        f"{DAEMON} q staking validators --node {RPC} --chain-id {CHAINID} --output json"
    )
    return exec_command(command)


# `fetch_validator_pubkey_from_node` takes validator home dir as param and
# internally calls the `show-validator` to get node's tendermint validator info.
def fetch_validator_pubkey_from_node(val_home_dir):
    command = f"{DAEMON} tendermint show-validator --home {val_home_dir}"
    return exec_command(command)
