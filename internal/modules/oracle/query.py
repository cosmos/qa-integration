from utils import exec_command, env

DAEMON = env.DAEMON
RPC = env.RPC
CHAINID = env.CHAINID

# query_exchange_rates queries the prices of all exchange rates
def query_exchange_rates():
    command = f"""{DAEMON} q oracle exchange-rates --node {RPC} \
--chain-id {CHAINID} --output json"""
    return exec_command(command)

# query_exchange_rate queries the price of an exchange rate
def query_exchange_rate(asset):
    command = f"""{DAEMON} q oracle exchange-rate ${asset} --node {RPC} \
--chain-id {CHAINID} --output json"""
    return exec_command(command)

def query_aggregate_prevote(valAddress):
    command = f"""{DAEMON} q oracle aggregate-prevotes ${valAddress} --node {RPC} \
--chain-id {CHAINID} --output json"""
    return exec_command(command)

def query_aggregate_vote(valAddress):
    command = f"""{DAEMON} q oracle aggregate-votes ${valAddress} --node {RPC} \
--chain-id {CHAINID} --output json"""
    return exec_command(command)

def query_feeder_delegation(valAddress):
    command = f"""{DAEMON} q oracle feeder-delegation ${valAddress} --node {RPC} \
--chain-id {CHAINID} --output json"""
    return exec_command(command)

def query_miss_counter(valAddress):
    command = f"""{DAEMON} q oracle miss-counter ${valAddress} --node {RPC} \
--chain-id {CHAINID} --output json"""
    return exec_command(command)


def query_params():
    command = f"""{DAEMON} q oracle params --node {RPC} \
--chain-id {CHAINID} --output json"""
    return exec_command(command)
