import os, json

from utils import exec_command
from stats import QUERY_TYPE

DAEMON = os.getenv("DAEMON")
RPC = os.getenv("RPC")
CHAINID = os.getenv("CHAINID")

# The function 'query_staking_validators' fetches the validators information.
def query_staking_validators(test_type=None):
    try:
        command = f"{DAEMON} q staking validators --node {RPC} --chain-id {CHAINID} --output json"
        validators, validatorserr = exec_command(command, test_type, QUERY_TYPE)
        if len(validatorserr):
            return False, validatorserr
        return True, json.loads(validators)
    except Exception as e:
        return False, e


# The function `query_staking_delegations` fetches the information about the delagator delegations for a validator.
def query_staking_delegations(delegator, validator, test_type=None):
    try:
        command = f"{DAEMON} q staking delegation {delegator} {validator} --node {RPC} --chain-id {CHAINID} --output json"
        delegations, delegationerr = exec_command(command, test_type, QUERY_TYPE)
        if len(delegationerr):
            return False, delegationerr
        return True, json.loads(delegations)
    except Exception as e:
        return False, e
