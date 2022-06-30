import os
from utils import exec_and_process_output, DEFAULT_GAS

DAEMON = os.getenv("DAEMON")
DAEMON_HOME = os.getenv("DAEMON_HOME")
RPC = os.getenv("RPC")
CHAINID = os.getenv("CHAINID")

# tx_submit_proposal internally calls the submit proposal transaction with given proposal type
# and return the response in json format.
def tx_submit_proposal(
    from_key,
    proposal_file_or_name,
    proposal_type="software-upgrade",
    gas=DEFAULT_GAS,
    unsigned=False,
    sequence=None,
    extra_args="",
):
    try:
        if unsigned:
            command = f"""{DAEMON} tx gov submit-proposal {proposal_type} {proposal_file_or_name} --chain-id {CHAINID} --output json --node {RPC} \
--generate-only --gas {gas}"""
            return exec_and_process_output(command, extra_args)
        else:
            if sequence != None:
                command = f"""{DAEMON} tx gov submit-proposal community-pool-spend {proposal_file_or_name} --chain-id {CHAINID} \
--keyring-backend test --from {from_key} --home {DAEMON_HOME}-1 --node {RPC} --output json -y --sequence {sequence} --gas {gas}"""
            else:
                command = f"""{DAEMON} tx gov submit-proposal community-pool-spend {proposal_file_or_name} --chain-id {CHAINID} --keyring-backend test \
 --home {DAEMON_HOME}-1 --from {from_key} --node {RPC} --output json -y --gas {gas}"""
            status, tx = exec_and_process_output(command, extra_args)
            if status and tx["code"] != 0:
                return False, tx
            return status, tx
    except Exception as e:
        return False, e


# tx_cancel_software_upgrade internally calls the cancel software upgrade tx command
# and return the response in json format.
def tx_cancel_software_upgrade(
    from_key,
    gas=DEFAULT_GAS,
    unsigned=False,
    sequence=None,
    extra_args="",
):
    try:
        if unsigned:
            command = f"""{DAEMON} tx gov submit-proposal cancel-software-upgrade --chain-id {CHAINID} --output json --node {RPC} \
--generate-only --gas {gas}"""
            return exec_and_process_output(command, extra_args)
        else:
            if sequence != None:
                command = f"""{DAEMON} tx gov submit-proposal cancel-software-upgrade --chain-id {CHAINID} \
--keyring-backend test --from {from_key} --home {DAEMON_HOME}-1 --node {RPC} --output json -y --sequence {sequence} --gas {gas}"""
            else:
                command = f"""{DAEMON} tx gov submit-proposal cancel-software-upgrade --chain-id {CHAINID} --keyring-backend test \
 --home {DAEMON_HOME}-1 --from {from_key} --node {RPC} --output json -y --gas {gas}"""
            status, tx = exec_and_process_output(command, extra_args)
            if status and tx["code"] != 0:
                return False, tx
            return status, tx
    except Exception as e:
        return False, e


# tx_deposit internally calls the 'gov deposit' tx command and return the response in json format
def tx_deposit(
    from_key,
    proposal_id,
    deposit,
    gas=DEFAULT_GAS,
    unsigned=False,
    sequence=None,
    extra_args="",
):
    try:
        if unsigned:
            command = f"{DAEMON} tx gov deposit {proposal_id} {deposit} --chain-id {CHAINID} --output json --node {RPC} --generate-only --gas {gas}"
            return exec_and_process_output(command, extra_args)
        else:
            if sequence != None:
                command = f"""{DAEMON} tx gov deposit {proposal_id} {deposit} --chain-id {CHAINID} \
--keyring-backend test --from {from_key} --home {DAEMON_HOME}-1 --node {RPC} --output json -y --sequence {sequence} --gas {gas}"""
            else:
                command = f"""{DAEMON} tx gov deposit {proposal_id} {deposit} --chain-id {CHAINID} --keyring-backend test \
 --home {DAEMON_HOME}-1 --from {from_key} --node {RPC} --output json -y --gas {gas}"""
            status, tx = exec_and_process_output(command, extra_args)
            if status and tx["code"] != 0:
                return False, tx
            return status, tx
    except Exception as e:
        return False, e


# tx_vote internally calls the 'gov vote' tx command and return the response in json format
def tx_vote(
    from_key,
    proposal_id,
    option,
    gas=DEFAULT_GAS,
    unsigned=False,
    sequence=None,
    extra_args="",
):
    try:
        if unsigned:
            command = f"{DAEMON} tx gov vote {proposal_id} {option} --chain-id {CHAINID} --output json --node {RPC} --generate-only --gas {gas}"
            return exec_and_process_output(command, extra_args)
        else:
            if sequence != None:
                command = f"""{DAEMON} tx gov vote {proposal_id} {option} --chain-id {CHAINID} \
--keyring-backend test --from {from_key} --home {DAEMON_HOME}-1 --node {RPC} --output json -y --sequence {sequence} --gas {gas}"""
            else:
                command = f"""{DAEMON} tx gov vote {proposal_id} {option} --chain-id {CHAINID} --keyring-backend test \
 --home {DAEMON_HOME}-1 --from {from_key} --node {RPC} --output json -y --gas {gas}"""
            status, tx = exec_and_process_output(command, extra_args)
            if status and tx["code"] != 0:
                return False, tx
            return status, tx
    except Exception as e:
        return False, e


# tx_weighted_vote internally calls the 'gov weighted_vote' tx command and return the response in json format
def tx_weighted_vote(
    from_key,
    proposal_id,
    options,
    gas=DEFAULT_GAS,
    unsigned=False,
    sequence=None,
    extra_args="",
):
    try:
        if unsigned:
            command = f"{DAEMON} tx gov weighted-vote {proposal_id} {options} --chain-id {CHAINID} --output json --node {RPC} --generate-only --gas {gas}"
            return exec_and_process_output(command, extra_args)
        else:
            if sequence != None:
                command = f"""{DAEMON} tx gov weighted-vote {proposal_id} {options} --chain-id {CHAINID} \
--keyring-backend test --from {from_key} --home {DAEMON_HOME}-1 --node {RPC} --output json -y --sequence {sequence} --gas {gas}"""
            else:
                command = f"""{DAEMON} tx gov weighted-vote {proposal_id} {options} --chain-id {CHAINID} --keyring-backend test \
 --home {DAEMON_HOME}-1 --from {from_key} --node {RPC} --output json -y --gas {gas}"""
            status, tx = exec_and_process_output(command, extra_args)
            if status and tx["code"] != 0:
                return False, tx
            return status, tx
    except Exception as e:
        return False, e
