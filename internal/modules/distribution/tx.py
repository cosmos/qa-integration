from cgi import print_arguments
from utils import exec_command
import os
import json

DAEMON = os.getenv('DAEMON')
DENOM = os.getenv('DENOM')
DEFAULT_GAS = 2000000
CHAINID = os.getenv('CHAINID')
RPC = os.getenv('RPC')
DAEMON_HOME = os.getenv('DAEMON_HOME')

# tx_withdraw_rewards takes from_key,validator address as parameters and executes 
# 'withdraw-rewards' command and returns response in json formate
def tx_withdraw_rewards(from_key,validator_addr,gas={DEFAULT_GAS},unsigned = False,sequence = None):
    if unsigned:
        command = f"{DAEMON} tx distribution withdraw-rewards {validator_addr} --from {from_key} --chain-id {CHAINID} --output json --node {RPC}"
    else: 
        if sequence is not None:
            command = f"{DAEMON} tx distribution withdraw-rewards {validator_addr} --from {from_key} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --sequence {sequence}"
        else:
            command = f"{DAEMON} tx distribution withdraw-rewards {validator_addr} --from {from_key} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y"
    return exec_command(command)

# tx_withdraw_commision_rewards takes from_key,validator_addr as parameters and executes
# 'withdraw-rewards' with 'commission' flag and returns response in json formate
def tx_withdraw_commision_rewards(from_key,validator_addr,gas={DEFAULT_GAS},unsigned = False,sequence = None):
    if unsigned:
        command = f"{DAEMON} tx distribution withdraw-rewards {validator_addr} --from {from_key} --commission --chain-id {CHAINID} --output json --node {RPC} --generate-only --gas {gas}"
    else: 
        if sequence is not None:
            command = f"{DAEMON} tx distribution withdraw-rewards {validator_addr} --from {from_key} --commission --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --sequence {sequence} --gas {gas}"
        else:
            command = f"{DAEMON} tx distribution withdraw-rewards {validator_addr} --from {from_key} --commission --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y"
    return exec_command(command)

# tx_withdraw_allrewards takes from_key as parameters and executes 'withdraw-all-rewards'
# and returns response in json formate
def tx_withdraw_allrewards(from_key,gas={DEFAULT_GAS},unsigned = False,sequence = None):
    if unsigned:
        command = f"{DAEMON} tx distribution withdraw-all-rewards --from {from_key} --chain-id {CHAINID} --output json --node {RPC} --generate-only --gas {gas}"
    else:
        if sequence is not None:
            command = f"{DAEMON} tx distribution withdraw-all-rewards --from {from_key} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --sequence {sequence}"
        else:
            command = f"{DAEMON} tx distribution withdraw-all-rewards --from {from_key} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y"
    return exec_command(command)

# tx_fund_communitypool takes from_key as parameter and executes 
# fund-community-pool command returns response in json formate
def tx_fund_communitypool(from_key,amount,gas={DEFAULT_GAS},unsigned = False,sequence = None):
    if unsigned:
        command = f"{DAEMON} tx distribution fund-community-pool {amount}{DENOM} --from {from_key} --chain-id {CHAINID} --output json --node {RPC} --generate-only"
    else:
        if sequence is not None:
            command = f"{DAEMON} tx distribution fund-community-pool {amount}{DENOM} --from {from_key} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --sequence {sequence}"
        else:
            command = f"{DAEMON} tx distribution fund-community-pool {amount}{DENOM} --from {from_key} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y"
    return exec_command(command)

# tx_set_withdraw_addr takes from_key and withdrawer addres as parameters 
# executes 'set-withdraw-addr' and returns response in json formate 
def tx_set_withdraw_addr(from_key,withdraw_addr,gas={DEFAULT_GAS},unsigned = False,sequence = None):
    if unsigned:
        command = f"{DAEMON} tx distribution set-withdraw-addr {withdraw_addr} --from {from_key} --chain-id {CHAINID} --output json --node {RPC} --generate-only --output json"     
    else:
        if sequence is not None:
            command = f"{DAEMON} tx distribution set-withdraw-addr {withdraw_addr} --from {from_key} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --sequence {sequence}"
        else:
            command = f"{DAEMON} tx distribution set-withdraw-addr {withdraw_addr} --from {from_key} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y"
    return exec_command(command)
