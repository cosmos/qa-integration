import os, json
from utils.commands import command_processor

DAEMON = os.getenv('DAEMON')

def fetch_staking_validators(RPC):
    command = f"{DAEMON} q staking validators --node {RPC} --output json"
    validators, validatorserr = command_processor(command)
    if not len(validatorserr):
        validators = json.loads(validators)
    return validators, validatorserr

def fetch_staking_delegations(From, to, RPC):
    command = f"{DAEMON} q staking delegation {From} {to} --node {RPC} --output json"
    delegations, delegationerr = command_processor(command)
    if not len(delegationerr):
        delegations = json.loads(delegations)
    return delegations, delegationerr
    