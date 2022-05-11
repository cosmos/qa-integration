import os,json
from core.tx import tx_broadcast, tx_sign
from modules.bank.tx import tx_send
from utils.commands import exec_command

CHAINID = os.getenv('CHAINID')
DAEMON = os.getenv('DAEMON')
DAEMON_HOME = os.getenv('DAEMON_HOME')
DENOM = os.getenv('DENOM')
HOME = os.getenv('HOME')
RPC = os.getenv('RPC')

def unsigned_tx(from_address, to_address, file_name):
    try:
        status, unsignedTx = tx_send(from_address, to_address, amount = 1000000, gas = 500000, unsigned = True)
        if not status:
            return status, unsignedTx 
        with open(f"{HOME}/{file_name}", 'w') as outfile:
            json.dump(unsignedTx, outfile)
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
            

def signed_tx(unsigned_file, signed_file, from_address, sequence):
    try:
        status, signTx = tx_sign(unsigned_file, from_address, sequence, 500000)
        if not status:
            return status, signTx
        with open(f'{HOME}/{signed_file}', 'w') as outfile:
            json.dump(signTx, outfile)
            
        status, broadcast_response = tx_broadcast(signed_file, 500000, 'async')
        if not status:
            return status, broadcast_response
        return status, broadcast_response['txhash']
    except Exception as e:
        return False, e

    


    