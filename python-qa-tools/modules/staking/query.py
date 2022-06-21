import os, json
from utils import exec_command

DAEMON = os.getenv("DAEMON")
RPC = os.getenv("RPC")
CHAINID = os.getenv("CHAINID")

# The function 'query_staking_validators' fetches the validators information.
def query_staking_validators():
    try:
        command = f"{DAEMON} q staking validators --node {RPC} --chain-id {CHAINID} --output json"
        validators, validatorserr = exec_command(command)
        if len(validatorserr):
            return False, validatorserr
        return True, json.loads(validators)
    except Exception as e:
        return False, e


# The function `query_staking_delegations` fetches the information about the delagator delegations for a validator.
def query_staking_delegations(delegator, validator):
    try:
        command = f"{DAEMON} q staking delegation {delegator} {validator} --node {RPC} --chain-id {CHAINID} --output json"
        delegations, delegationerr = exec_command(command)
        if len(delegationerr):
            return False, delegationerr
        return True, json.loads(delegations)
    except Exception as e:
        return False, e

# `query_all_delegations` fetches all redelegation records for an individual delegator.   
def query_all_redelegations(delegator_addr):
    try:
        command = f"{DAEMON} q staking redelegations {delegator_addr} --node {RPC} --chain-id {CHAINID} --output json"
        redelegations, err = exec_command(command)
        if len(err):
            return False, err
        return True, json.loads(redelegations)
    except Exception as e:
        return False, e

# `query_staking_redelegation` query a redelegation record for an individual delegator between a source and destination validator.   
def query_staking_redelegation(delegator_addr, src_validator_addr, dst_validator_addr):
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
        redelegations, err = exec_command(command)
        if len(err):
            return False, err
        return True, json.loads(redelegations)
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