import os,json, sys
from utils.commands import command_processor

DAEMON = os.getenv('DAEMON')
DAEMON_HOME = os.getnev('DAEMON_HOME')
DENOM = os.getenv('DENOM')
CHAINID = os.getenv('CHAINID')
HOME = os.getnev('HOME')

def fetch_seq_no(address, RPC):
    command = f"{DAEMON} q account {address} --node {RPC} --output json"
    seq, seqerr = command_processor(command)
    if len(seqerr):
        return False, seqerr
    seq = json.loads(seq)
    return True, int(seq['sequence'])

def unsigned_tx(from_address, to_address, file_name):
    try:
        command = f"{DAEMON} tx bank send {from_address} {to_address} 1000000{DENOM} --chain-id {CHAINID} --output json --generate-only --gas 500000"
        unsignedTx, unsignedTxerr = command_processor(command)
        if len(unsignedTxerr):
            return False, unsignedTxerr
        with open(f"{HOME}/{file_name}", 'w') as outfile:
            json.dump(json.loads(unsignedTx), outfile)
        return True, unsignedTx
    except Exception as e:
        return False, e
    
def write_json(file_name):
    with open(f"{HOME}/{file_name}", 'r+') as file:
            file_data = json.load(file)
            new_data = file_data["body"]["messages"][-1]
            file_data["body"]["messages"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent = 4)
            

def signed_tx(unsigned_file, signed_file, from_address, sequence, RPC):
    try:
        command = f"{DAEMON} tx sign {HOME}/{unsigned_file} --from {from_address} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --signature-only=false --sequence {sequence} --gas 500000"
        signTx, signTxerr = command_processor(command)
        if len(signTxerr):
            return False, signTxerr
        with open(f'{HOME}/{signed_file}', 'w') as outfile:
            json.dump(json.loads(signTx), outfile)
            
        command = f"{DAEMON} tx broadcast {HOME}/{signed_file} --output json --chain-id {CHAINID} --gas 500000 --node {RPC} --broadcast-mode async"
        broadcastTx, broadcasterr = command_processor(command)
        if len(broadcasterr):
            return False, broadcasterr
        broadcastTx = json.loads(broadcastTx)
        return True, broadcastTx['txhash']
    except Exception as e:
        return False, e

    


    