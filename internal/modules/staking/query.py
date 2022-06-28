import json

from utils import exec_command, env

DAEMON = env.DAEMON
RPC = env.RPC
CHAINID = env.CHAINID

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
