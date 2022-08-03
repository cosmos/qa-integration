from utils import exec_command, env

DAEMON = env.DAEMON
RPC = env.RPC
CHAINID = env.CHAINID

# query_deposits queries deposits on a proposal
def query_deposits(proposal_id, extra_args=""):
    command = f"""{DAEMON} q gov deposits {proposal_id} --node {RPC} \
--chain-id {CHAINID} --output json"""
    return exec_command(command, extra_args)


# query_deposit queries details of a deposit with
# specific deposit address and proposal id
def query_deposit(proposal_id, deposit_addr, extra_args=""):
    command = f"""{DAEMON} q gov deposit {proposal_id} {deposit_addr} \
--node {RPC} --chain-id {CHAINID} --output json"""
    return exec_command(command, extra_args)


# query_params queries the parameters of the governance process
def query_params(extra_args=""):
    command = f"""{DAEMON} q gov params --node {RPC} \
--chain-id {CHAINID} --output json"""
    return exec_command(command, extra_args)


# query_param queries the specific parameter
# voting|tallying|deposit of the governance process
def query_param(param_type, extra_args=""):
    command = f"""{DAEMON} q gov param {param_type} --node {RPC} \
--chain-id {CHAINID} --output json"""
    return exec_command(command, extra_args)


# query_proposals queries all proposals
def query_proposals(extra_args=""):
    command = (
        f"{DAEMON} q gov proposals --node {RPC} --chain-id {CHAINID} --output json"
    )
    return exec_command(command, extra_args)


# query_proposal queries a proposal with given proposal id
def query_proposal(proposal_id, extra_args=""):
    command = f"""{DAEMON} q gov proposal {proposal_id} --node {RPC} \
--chain-id {CHAINID} --output json"""
    return exec_command(command, extra_args)


# query_proposer queries address who proposed proposal
def query_proposer(proposal_id, extra_args=""):
    command = f"""{DAEMON} q gov proposer {proposal_id} --node {RPC} \
--chain-id {CHAINID} --output json"""
    return exec_command(command, extra_args)


# query_tally queries tally of votes on a proposal
def query_tally(proposal_id, extra_args=""):
    command = f"{DAEMON} q gov tally {proposal_id} --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command, extra_args)


# query_votes queries votes on a proposal with given proposal id
def query_votes(proposal_id, extra_args=""):
    command = f"{DAEMON} q gov votes {proposal_id} --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command, extra_args)


# query_vote queries details of a vote with specific vote address and proposal id
def query_vote(proposal_id, vote_addr, extra_args=""):
    command = f"""{DAEMON} q gov vote {proposal_id} {vote_addr} \
--node {RPC} --chain-id {CHAINID} --output json"""
    return exec_command(command, extra_args)


# TODO: use instead query plan from upgrade module  # pylint: disable=fixme
# when method is added, query_upgrade_plan queries upgrade plan
def query_upgrade_plan(extra_args=""):
    command = f"{DAEMON} q upgrade plan --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command, extra_args)
