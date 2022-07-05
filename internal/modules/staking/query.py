import os, json
from utils import exec_command

DAEMON = os.getenv("DAEMON")
RPC = os.getenv("RPC")
CHAINID = os.getenv("CHAINID")

# 'query_staking_validators' fetches the validators information.
def query_staking_validators():
    try:
        command = f"{DAEMON} q staking validators --node {RPC} --chain-id {CHAINID} --output json"
        validators, validators_err = exec_command(command)
        if len(validators_err):
            return False, validators_err
        return True, json.loads(validators)
    except Exception as e:
        return False, e


# `query_delegator_delegations` fetches the information about the delagator delegations for a validator.
def query_delegator_delegations(delegator, validator):
    try:
        command = f"{DAEMON} q staking delegation {delegator} {validator} --node {RPC} --chain-id {CHAINID} --output json"
        delegations, delegation_err = exec_command(command)
        if len(delegation_err):
            return False, delegation_err
        return True, json.loads(delegations)
    except Exception as e:
        return False, e


# `query_delegator_redelegations` fetches all redelegation records for an individual delegator.
def query_delegator_redelegations(delegator_addr):
    try:
        command = f"{DAEMON} q staking redelegations {delegator_addr} --node {RPC} --chain-id {CHAINID} --output json"
        redelegations, err = exec_command(command)
        if len(err):
            return False, err
        return True, json.loads(redelegations)
    except Exception as e:
        return False, e


# `query_delegator_redelegation` query a redelegation record for an individual delegator between a source and destination validator.
def query_delegator_redelegation(delegator_addr, src_validator_addr, dst_validator_addr):
    try:
        command = f"{DAEMON} q staking redelegation {delegator_addr} {src_validator_addr} {dst_validator_addr} --node {RPC} --chain-id {CHAINID} --output json"
        redelegations, err = exec_command(command)
        if len(err):
            return False, err
        return True, json.loads(redelegations)
    except Exception as e:
        return False, e


# `query_unbonding_delegation` query unbonding delegations for an individual delegator on an individual validator.
def query_unbonding_delegation(delegator_addr, validator_addr):
    try:
        command = f"{DAEMON} q staking unbonding-delegation {delegator_addr} {validator_addr} --node {RPC} --chain-id {CHAINID} --output json"
        unbond_delegations, err = exec_command(command)
        if len(err):
            return False, err
        return True, json.loads(unbond_delegations)
    except Exception as e:
        return False, e


# `query_validator` query details about an individual validator.
def query_validator(validator_addr):
    try:
        command = f"{DAEMON} q staking validator {validator_addr} --node {RPC} --chain-id {CHAINID} --output json"
        validator, err = exec_command(command)
        if len(err):
            return False, err
        return True, json.loads(validator)
    except Exception as e:
        return False, e


# `query_validator_set` query details about all validators on a network.
def query_validator_set():
    try:
        command = f"{DAEMON} q staking validators --node {RPC} --chain-id {CHAINID} --output json"
        validators, err = exec_command(command)
        if len(err):
            return False, err
        return True, json.loads(validators)
    except Exception as e:
        return False, e

# `fetch_validator_pubkey_from_node` is to get node's tendermint validator info
def fetch_validator_pubkey_from_node(val_home_dir):
    command = f"{DAEMON} tendermint show-validator --home {val_home_dir}"
    key, err = exec_command(command)
    return key, err
