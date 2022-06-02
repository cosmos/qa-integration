import json, os
from core.tx import tx_broadcast, tx_sign
from utils import exec_command

DAEMON = os.getenv('DAEMON')
DENOM = os.getenv('DENOM')
CHAINID = os.getenv('CHAINID')
HOME = os.getenv('HOME')
DAEMON_HOME = os.getenv('DAEMON_HOME')
RPC = os.getenv('RPC')
DEFAULT_GAS = 2000000

def create_unsigned_txs(from_address, to_address, amount, file_name):
    try:
        status, unsignedTx = tx_send(from_address, to_address, amount, gas = DEFAULT_GAS, unsigned = True)
        if not status:
            return status, unsignedTx 
        with open(f"{HOME}/{file_name}", 'w') as outfile:
            json.dump(unsignedTx, outfile)
        return True, unsignedTx
    except Exception as e:
        return False, e

def create_signed_txs(unsigned_file, signed_file, from_address, sequence):
    try:
        status, signTx = tx_sign(unsigned_file, from_address, sequence, DEFAULT_GAS)
        if not status:
            return status, signTx
        with open(f'{HOME}/{signed_file}', 'w') as outfile:
            json.dump(signTx, outfile)
            
        status, broadcast_response = tx_broadcast(signed_file, DEFAULT_GAS, 'block')
        if not status:
            return status, broadcast_response
        return status, broadcast_response['txhash']
    except Exception as e:
        return False, e

def tx_send(from_address, to_address, amount, gas="auto", unsigned = False, sequence = None):
    try:    
        if unsigned:
            command = f"{DAEMON} tx bank send {from_address} {to_address} {amount}{DENOM} --chain-id {CHAINID} --output json --node {RPC} --generate-only --gas {gas}"
            Tx, Txerr = exec_command(command)
            if len(Txerr):
                return False, Txerr
            return True, json.loads(Tx)
        else:
            if sequence != None:
                command = f"{DAEMON} tx bank send {from_address} {to_address} {amount}{DENOM} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --sequence {sequence} --gas {gas}"
                
            else:
                command = f"{DAEMON} tx bank send {from_address} {to_address} {amount}{DENOM} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --gas {gas}"
            Tx, Txerr = exec_command(command)
            Tx = json.loads(Tx)
            if len(Txerr):
                return False, Txerr
            elif Tx['code'] != 0:
                return False, Tx
            return True, Tx
    except Exception as e:
        return False, e