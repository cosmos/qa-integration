import os,json, sys
from modules.bank.tx import tx_send, tx_sign
from utils.commands import exec_command

DAEMON = os.getenv('DAEMON')
DAEMON_HOME = os.getnev('DAEMON_HOME')
DENOM = os.getenv('DENOM')
CHAINID = os.getenv('CHAINID')
HOME = os.getnev('HOME')

def fetch_seq_no(address, RPC):
    command = f"{DAEMON} q account {address} --node {RPC} --output json"
    seq, seqerr = exec_command(command)
    if len(seqerr):
        return False, seqerr
    seq = json.loads(seq)
    return True, int(seq['sequence'])

def unsigned_tx(from_address, to_address, file_name):
    try:
        status, unsignedTx = tx_send(from_address, to_address, gas = 500000, unsigned = True, output = "json")
        if not status:
            return status, unsignedTx 
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
        status, signTx = tx_sign(unsigned_file, from_address, RPC, sequence, gas = 500000)
        if not status:
            return status, signTx
        with open(f'{HOME}/{signed_file}', 'w') as outfile:
            json.dump(json.loads(signTx), outfile)
            
        command = f"{DAEMON} tx broadcast {HOME}/{signed_file} --output json --chain-id {CHAINID} --gas 500000 --node {RPC} --broadcast-mode async"
        broadcastTx, broadcasterr = exec_command(command)
        if len(broadcasterr):
            return False, broadcasterr
        broadcastTx = json.loads(broadcastTx)
        return True, broadcastTx['txhash']
    except Exception as e:
        return False, e

    


    