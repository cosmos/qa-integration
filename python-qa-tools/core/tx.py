import os, json
from utils.commands import exec_command

CHAINID = os.getenv('CHAINID')
DAEMON = os.getenv('DAEMON')
DAEMON_HOME = os.getenv('DAEMON_HOME')
HOME = os.getenv('HOME')
RPC = os.getenv('RPC')

def tx_sign(unsigned_file_name, from_address, sequence, gas):
    try:
        command = f"{DAEMON} tx sign {HOME}/{unsigned_file_name} --from {from_address} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --signature-only=false --sequence {sequence} --gas {gas} --output json"
        signTx, signTxerr = exec_command(command)
        if len(signTxerr):
            return False, signTxerr
        return True, json.loads(signTx) 
    except Exception as e:
        return False, e
    
def tx_broadcast(signed_file, gas, broadcast_mode = "sync"):
    try:
        command = f"{DAEMON} tx broadcast {HOME}/{signed_file} --output json --chain-id {CHAINID} --gas {gas} --node {RPC} --broadcast-mode {broadcast_mode} --output json"
        broadcastTx, broadcasterr = exec_command(command)
        if len(broadcasterr):
            return False, broadcasterr
        return True, json.loads(broadcastTx)
    except Exception as e:
        return False, e