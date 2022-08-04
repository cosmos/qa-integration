from internal.utils import exec_command, env

DAEMON = env.DAEMON
RPC = env.RPC
CHAINID = env.CHAINID

# 'query_module_version' quereis the respective module's consensus versions..
def query_module_version(module_name):
    command = (
        f"{DAEMON} q upgrade module_versions {module_name} --node {RPC} --output json"
    )
    return exec_command(command)


# 'query_module_versions' quereis all the module's consensus versions..
def query_module_versions():
    command = f"{DAEMON} q upgrade module_versions --node {RPC} --output json"
    return exec_command(command)


# query_vote queries details of a vote with specific vote address and proposal id
def query_vote(proposal_id, vote_addr, extra_args=""):
    command = f"{DAEMON} q gov vote {proposal_id} {vote_addr} --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command, extra_args)

# 'query_block' quereis the verified data of a block.
def query_block():
    command = (
        f"{DAEMON} q block --node {RPC}"
    )
    return exec_command(command)

# 'query_proposals' quereis all proposal details.
def query_proposals():
    command = (
        f"{DAEMON} q gov proposals --node {RPC} --output json"
    )
    return exec_command(command)

# 'query_upgrade' quereis details of the header for the block at which it was applied.
def query_upgrade(upgrade_name):
    command = (
        f"{DAEMON} q upgrade applied {upgrade_name} --node {RPC} --chain-id {CHAINID}  --output json"
    )
    return exec_command(command)

# 'query_upgrade_plan' quereis the currently scheduled upgrade plan, if one exists.
def query_upgrade_plan():
    command = (
        f"{DAEMON} q upgrade plan --node {RPC} --chain-id {CHAINID}  --output json"
    )
    return exec_command(command)

# 'query_proposal' quereis proposal details.
def query_proposal(porposal_id):
    command = (
        f"{DAEMON} q gov proposal {porposal_id} --node {RPC} --chain-id {CHAINID} --output json"
    )
    return exec_command(command)
