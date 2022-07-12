import json,os
from utils import exec_command

DAEMON = os.getenv('DAEMON')
RPC = os.getenv('RPC')
CHAINID = os.getenv('CHAINID')

# query_commissio_rewards fetches validator commission rewards and return response in json formate
def query_commission_rewards(validator_addr):
    command = f"{DAEMON} q distribution commission {validator_addr} --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)

# query_community_pool fetches community pool fund and return response in json formate
def query_community_pool():
    command = f"{DAEMON} q distribution community-pool --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)

# query_params fetches distribution module params and returns response in json formate
def query_params():
    command = f"{DAEMON} q distribution params --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)

def query_rewards_singleval(delegator_addr,validator_addr):
   command = f"{DAEMON} q distribution rewards {delegator_addr} {validator_addr} --node {RPC} --chain-id {CHAINID} --output json"
   return exec_command(command)

# query_rewards fetches rewards and returns response in json formate
def query_rewards(delegator_addr):
    command = f"{DAEMON} q distribution rewards {delegator_addr} --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)

# query_slashes fetches validator's slashes info and returns response in json formate
def query_slashes(validator_addr,start_height,end_height):
   command = f"{DAEMON} q distribution slashes {validator_addr} {start_height} {end_height} --node {RPC} --chain-id {CHAINID} --output json"
   return exec_command(command)

# query_validator_outstanding_rewards fetches validator's outstanding rewards and returns response in json formate
def query_validator_outstanding_rewards(validator_addr):
    command = f"{DAEMON} q distribution validator-outstanding-rewards {validator_addr} --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)

def query_delegation(delegator,validator):
    command = f"{DAEMON} q staking delegation {delegator} {validator} --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)

def query_delegations(delegator):
    command = f"{DAEMON} q staking delegations {delegator} --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)