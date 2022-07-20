from utils import exec_command, env

DAEMON = env.DAEMON
DENOM = env.DENOM
CHAINID = env.CHAINID
HOME = env.HOME
DAEMON_HOME = env.DAEMON_HOME
RPC = env.RPC
DEFAULT_GAS = env.DEFAULT_GAS

# tx_withdraw_rewards takes from_key,validator address as parameters and executes
# 'withdraw-rewards' command and returns response in json formate
def tx_withdraw_rewards(from_key, validator_addr):

    command = f"{DAEMON} tx distribution withdraw-rewards {validator_addr} --from {from_key} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y"
    return exec_command(command)


# tx_withdraw_commision_rewards takes from_key,validator_addr as parameters and executes
# 'withdraw-rewards' with 'commission' flag and returns response in json formate
def tx_withdraw_commision_rewards(from_key, validator_addr):

    command = f"{DAEMON} tx distribution withdraw-rewards {validator_addr} --from {from_key} --commission --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y"
    return exec_command(command)


# tx_withdraw_allrewards takes from_key as parameters and executes 'withdraw-all-rewards'
# and returns response in json formate
def tx_withdraw_allrewards(from_key):

    command = f"{DAEMON} tx distribution withdraw-all-rewards --from {from_key} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y"
    return exec_command(command)


# tx_fund_communitypool takes from_key as parameter and executes
# fund-community-pool command returns response in json formate
def tx_fund_communitypool(from_key, amount):

    command = f"{DAEMON} tx distribution fund-community-pool {amount}{DENOM} --from {from_key} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y"
    return exec_command(command)


# tx_set_withdraw_addr takes from_key and withdrawer addres as parameters
# executes 'set-withdraw-addr' and returns response in json formate
def tx_set_withdraw_addr(from_key, withdraw_addr):

    command = f"{DAEMON} tx distribution set-withdraw-addr {withdraw_addr} --from {from_key} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y"
    return exec_command(command)
