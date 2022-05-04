import os
from utils.commands import exec_command
DAEMON = os.getenv('DAEMON')
DENOM = os.getenv('DENOM')
CHAINID = os.getenv('DENOM')

def tx_send(from_address, to):
    command = f"{DAEMON} tx bank send {from_address} {to} 1000000{DENOM} --chain-id {CHAINID} --output json --generate-only --gas 500000"
    unsignedTx, unsignedTxerr = exec_command(command)
    if len(unsignedTxerr):
        return False, unsignedTxerr
    return True, unsignedTx