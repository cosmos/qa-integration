import os, json
from utils.commands import exec_command

DAEMON = os.getenv('DAEMON')

def fetch_staking_validators(RPC):
    command = f"{DAEMON} q staking validators --node {RPC} --output json"
    validators, validatorserr = exec_command(command)
    if not len(validatorserr):
        validators = json.loads(validators)
    return validators, validatorserr

def fetch_staking_delegations(From, to, RPC):
    command = f"{DAEMON} q staking delegation {From} {to} --node {RPC} --output json"
    delegations, delegationerr = exec_command(command)
    if not len(delegationerr):
        delegations = json.loads(delegations)
    return delegations, delegationerr
    