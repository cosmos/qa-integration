import os
from utils import exec_command

DAEMON = os.getenv('DAEMON')
RPC = os.getenv('RPC')
CHAINID = os.getenv('CHAINID')

# query_annual_provision fetches current minting annual provision value and returns response in json formate
def query_annual_provision():
    command = f"{DAEMON} q mint annual-provisions --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)

# query_inflation fetches current minting inflation value and returns response in json formate
def query_inflation():
    command = f"{DAEMON} q mint inflation --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)

# query_params fetches mint module params
def query_params():
    command = f"{DAEMON} q mint params --node {RPC} --chain-id {CHAINID} --output json"
    return exec_command(command)

