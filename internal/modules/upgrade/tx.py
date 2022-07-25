import os
from internal.modules.staking.tx import DENOM
from utils import exec_command, env

DAEMON = env.DAEMON
DAEMON_HOME = env.DAEMON_HOME
RPC = env.RPC
CHAINID = env.CHAINID
DEFAULT_GAS = env.DEFAULT_GAS


# tx_submit_proposal internally calls the submit proposal transaction with given proposal type
# and return the response in json format.
def tx_submit_proposal(
    from_key,
    UPGRADE_NAME,
    UPGRADE_HEIGHT,
):
#tx gov submit-proposal software-upgrade $UPGRADE_NAME --title $UPGRADE_NAME \
#    --description upgrade --upgrade-height $((CURRENT_BLOCK_HEIGHT + 80)) --deposit 10000000$DENOM \
#    --from validator1 --yes --keyring-backend test --home $DAEMON_HOME-1 --node $RPC --chain-id $CHAINID
    command = f"""{DAEMON} tx gov submit-proposal software-upgrade {UPGRADE_NAME} --title {UPGRADE_NAME}
    --description upgrade --upgrade-height {UPGRADE_HEIGHT} --deposit 10000000{DENOM} --from {from_key}
    --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y"""
    print(f"command..............{command}")
    return exec_command(command)

# tx_vote internally calls the 'gov vote' tx command and return the response in json format
def tx_vote(
    from_key,
    proposal_id,
    option,
    gas=DEFAULT_GAS,
    home=f"{DAEMON_HOME}-1",
):
    command = f"""{DAEMON} tx gov vote {proposal_id} {option} --chain-id {CHAINID} --keyring-backend test
 --home {home} --from {from_key} --node {RPC} --output json -y --gas {gas}"""
    return exec_command(command)