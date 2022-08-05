import time
from utils import exec_command, env
from internal.modules.gov.query import query_proposals, query_proposal, query_proposer, query_deposits, query_deposit, query_votes, query_vote, query_tally
from internal.core.keys import keys_show

YES_VOTE = "VOTE_OPTION_YES"
NO_VOTE = "VOTE_OPTION_NO"
DENOM = env.DENOM
DAEMON = env.DAEMON
DAEMON_HOME = env.DAEMON_HOME
RPC = env.RPC
CHAINID = env.CHAINID
DEFAULT_GAS = env.DEFAULT_GAS

# tx_submit_proposal internally calls the submit proposal transaction with given proposal type
# and return the response in json format.
def tx_submit_proposal(
    from_key,
    proposal_file_or_name,
    proposal_type="software-upgrade",
    gas=DEFAULT_GAS,
    extra_args="",
):
    command = f"""{DAEMON} tx gov submit-proposal {proposal_type} {proposal_file_or_name} \
--chain-id {CHAINID} --keyring-backend test \
--home {DAEMON_HOME}-1 --from {from_key} --node {RPC} --output json -y --gas {gas}"""
    print("tx_submit_proposal", command)
    return exec_command(command, extra_args)


# tx_cancel_software_upgrade internally calls the cancel software upgrade tx command
# and return the response in json format.
def tx_cancel_software_upgrade(
    from_key,
    gas=DEFAULT_GAS,
    extra_args="",
):
    command = f"""{DAEMON} tx gov submit-proposal cancel-software-upgrade \
--chain-id {CHAINID} --keyring-backend test \
--home {DAEMON_HOME}-1 --from {from_key} --node {RPC} --output json -y --gas {gas}"""
    return exec_command(command, extra_args)


# tx_deposit internally calls the 'gov deposit' tx command and return the response in json format
def tx_deposit(
    from_key,
    proposal_id,
    deposit,
    gas=DEFAULT_GAS,
    extra_args="",
):
    command = f"""{DAEMON} tx gov deposit {proposal_id} {deposit} \
--chain-id {CHAINID} --keyring-backend test \
--home {DAEMON_HOME}-1 --from {from_key} --node {RPC} --output json -y --gas {gas}"""
    return exec_command(command, extra_args)


# tx_vote internally calls the 'gov vote' tx command and return the response in json format
def tx_vote(
    from_key,
    proposal_id,
    option,
    gas=DEFAULT_GAS,
    home=f"{DAEMON_HOME}-1",
    extra_args="",
):
    command = f"""{DAEMON} tx gov vote {proposal_id} {option} \
--chain-id {CHAINID} --keyring-backend test \
--home {home} --from {from_key} --node {RPC} --output json -y --gas {gas}"""
    return exec_command(command, extra_args)


# tx_weighted_vote internally calls the 'gov weighted_vote' tx command
# and return the response in json format
def tx_weighted_vote(
    from_key,
    proposal_id,
    options,
    gas=DEFAULT_GAS,
    home=f"{DAEMON_HOME}-1",
    extra_args="",
):
    command = f"""{DAEMON} tx gov weighted-vote {proposal_id} {options} \
--chain-id {CHAINID} --keyring-backend test \
--home {home} --from {from_key} --node {RPC} --output json -y --gas {gas}"""
    return exec_command(command, extra_args)


# submit_and_pass_proposal submits proposal and pass it with deposit, vote txs
def submit_and_pass_proposal(
    proposal_file_or_name, proposal_type="software-upgrade", extra_args=""
):  # pylint: disable=R0915
    validator1_acc = keys_show("validator1", "acc")[1]
    validator2_acc = keys_show("validator2", "acc", f"{DAEMON_HOME}-2")[1]
    status = True
    # submit proposal
    if proposal_type == "cancel-software-upgrade":
        status, _ = tx_cancel_software_upgrade(
            validator1_acc["name"],
            extra_args=extra_args,
        )
    else:
        status, _ = tx_submit_proposal(
            validator1_acc["name"],
            proposal_file_or_name,
            proposal_type,
            extra_args=extra_args,
        )
    time.sleep(4)

    # query all proposals
    status, out = query_proposals()
    proposals = out["proposals"]
    proposals_len = len(proposals)

    # query single proposal
    proposal_id = int(proposals[proposals_len - 1]["proposal_id"])

    # add deposit to a proposal
    deposit_amount = "10000000"
    status, _ = tx_deposit(
        validator1_acc["name"],
        proposal_id,
        deposit_amount + DENOM,
    )
    time.sleep(4)

    # vote to a proposal
    vote_option = YES_VOTE
    status, out = tx_vote(
        validator1_acc["name"],
        proposal_id,
        vote_option,
    )
    time.sleep(4)

    # add weighted-vote to a proposal
    weight_vote_option = f"{YES_VOTE}=0.5,{NO_VOTE}=0.5"
    status, out = tx_weighted_vote(
        validator2_acc["name"],
        proposal_id,
        weight_vote_option,
        home=f"{DAEMON_HOME}-2",
    )
    time.sleep(4)

    return status, out
