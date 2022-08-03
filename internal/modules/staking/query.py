"""
This module queries staking sub commands.
"""
from internal.utils import exec_command, env

DAEMON = env.DAEMON
RPC = env.RPC
CHAINID = env.CHAINID

# `query_delegator_delegation` queries individual delegator's delegation
# associated with a validator.
def query_delegator_delegation(delegator, validator):
    """
    The function `query_delegator_delegation` fetches the information
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


# `query_delegator_delegations` queries delegations
# for an individual delegator on all validators.
def query_delegator_delegations(delegator):
    command = f"""{DAEMON} q staking delegations {delegator} \
--node {RPC} --chain-id {CHAINID} --output json --count-total"""
    return exec_command(command)


# `query_delegations_of_validator` queries
# delegations on an individual validator.
def query_delegations_of_validator(validator_addr):
    command = f"""{DAEMON} q staking delegations-to {validator_addr} \
--node {RPC} --chain-id {CHAINID} --output json --count-total"""
    return exec_command(command)


# `query_delegator_redelegations` takes delegator address ad params and
# internally calls the `staking redelegations` and
# returns response of an individual delegator in json format.
def query_delegator_redelegations(delegator_addr):
    """
    The function `query_delegator_redelegations` fetches the redelegations information.
    """
    command = f"{DAEMON} q staking redelegations {delegator_addr} \
--node {RPC} --chain-id {CHAINID} --output json --count-total"
    return exec_command(command)


# `query_delegator_redelegation` queries single redelegation
# record for an individual delegator between a source
# and destination validator.
def query_delegator_redelegation(
    delegator_addr, src_validator_addr, dst_validator_addr
):
    """
    The function `query_delegator_redelegation` fetches the information
    """
    command = f"{DAEMON} q staking redelegation {delegator_addr} \
{src_validator_addr} {dst_validator_addr} --node {RPC} \
--chain-id {CHAINID} --output json "
    return exec_command(command)


# `query_delegator_redelegations_from` queries delegations that are redelegating from a validator.
def query_redelegations_from_val(src_validator_addr):

    command = f"""{DAEMON} q staking redelegations-from {src_validator_addr} \
--node {RPC} --chain-id {CHAINID} --output json --count-total"""
    return exec_command(command)


# `query_unbonding_delegation` queries
# unbonding delegations for an individual
# delegator on an individual validator.
def query_unbonding_delegation(delegator_addr, validator_addr):
    """
    The function `query_unbonding_delegation` fetches the unbonding delegation information.
    """
    command = f"{DAEMON} q staking unbonding-delegation {delegator_addr} \
{validator_addr} --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)


# `query_unbonding_delegations` queries unbonding delegations of a delegator.
def query_unbonding_delegations(delegator_addr):
    command = f"""{DAEMON} q staking unbonding-delegations {delegator_addr} \
--node {RPC} --chain-id {CHAINID} --output json --count-total"""
    return exec_command(command)


# `query_unbonding_delegations_from` queries delegations that are unbonding from a validator.
def query_unbondings_from_val(validator_addr):
    command = f"""{DAEMON} q staking unbonding-delegations-from {validator_addr} \
--node {RPC} --chain-id {CHAINID} --output json --count-total"""
    return exec_command(command)


# `query_validator` queries details about an
# individual validator and return response in json format.
def query_validator(validator_addr):
    """
    The function `query_validator` fetches the validator information.
    """
    command = f"{DAEMON} q staking validator {validator_addr} \
--node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)


# `query_validator_set` returns details about all
# validators on a network in the form of json.
def query_validator_set():
    """
    The function `query_validator_set` fetches the validator set information.
    """
    command = f"{DAEMON} q staking validators --node {RPC} \
--chain-id {CHAINID} --output json --count-total"
    return exec_command(command)


# `fetch_validator_pubkey_from_node` takes validator
# home dir as param and
# internally calls the `show-validator` to get node's
# tendermint validator info.
def fetch_validator_pubkey_from_node(val_home_dir):
    """
    The function `fetch_validator_pubkey_from_node` fetches the public key of a validator.
    """
    command = f"{DAEMON} tendermint show-validator --home {val_home_dir}"
    return exec_command(command)


# `query_staking_pool` queries values for amounts stored in the staking pool.
def query_staking_pool():
    command = f"{DAEMON} q staking pool --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)


# `query_staking_params` queries values set as staking parameters.
def query_staking_params():
    command = (
        f"{DAEMON} q staking params --node {RPC} --chain-id {CHAINID} --output json"
    )
    return exec_command(command)
