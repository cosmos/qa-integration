import os
from utils.commands import exec_command
DAEMON = os.getenv('DAEMON')
DENOM = os.getenv('DENOM')
CHAINID = os.getenv('DENOM')
HOME = os.getenv('HOME')
DAEMON_HOME = os.getenv('DAEMON_HOME')

def tx_send(from_address, to, gas, unsigned = False, output = None):
    if not output or output == "json":
        output = "json"
    elif output != "text" and output != "json":
        return False, {
            "Error": "output must be given either \"json\" or \"text\""
        }    
    if not unsigned:
        command = f"{DAEMON} tx bank send {from_address} {to} 1000000{DENOM} --chain-id {CHAINID} --output {output} --generate-only --gas {gas}"
    else:
        command = f"{DAEMON} tx bank send {from_address} {to} 1000000{DENOM} --chain-id {CHAINID} --output {output} --gas {gas}"
    unsignedTx, unsignedTxerr = exec_command(command)
    if len(unsignedTxerr):
        return False, unsignedTxerr
    return True, unsignedTx


def tx_sign(unsigned_file_name, from_address, node, sequence, gas):
    command = f"{DAEMON} tx sign {HOME}/{unsigned_file_name} --from {from_address} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {node} --signature-only=false --sequence {sequence} --gas {gas}"
    signTx, signTxerr = exec_command(command)
    if len(signTxerr):
        return False, signTxerr
    return True, signTx