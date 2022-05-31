import os, json

from utils import exec_command

DAEMON = os.getenv('DAEMON')
RPC = os.getenv('RPC')
CHAINID = os.getenv('CHAINID')

def query_staking_validators():
    try:
        command = f"{DAEMON} q staking validators --node {RPC} --chain-id {CHAINID} --output json"
        validators, validatorserr = exec_command(command)
        if len(validatorserr):
            return False, validatorserr
        return True, json.loads(validators)
    except Exception as e:
        return False, e
    
    
def query_staking_delegations(delegator, validator):
    try:
        command = f"{DAEMON} q staking delegation {delegator} {validator} --node {RPC} --chain-id {CHAINID} --output json"
        delegations, delegationerr = exec_command(command)
        if len(delegationerr):
            return False, delegationerr
        return True, json.loads(delegations)
    except Exception as e:
        return False, e