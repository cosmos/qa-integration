import json, os
from core.tx import tx_broadcast, tx_sign
from utils import exec_command

DAEMON = os.getenv("DAEMON")
DENOM = os.getenv("DENOM")
CHAINID = os.getenv("CHAINID")
HOME = os.getenv("HOME")
DAEMON_HOME = os.getenv("DAEMON_HOME")
RPC = os.getenv("RPC")
DEFAULT_GAS = 2000000

# 'create_unsigned_txs' takes sender(from_address), receiver(to_address), amount and file_name as parameters and call the function tx_send
# internally and stores the json to file_name file.
def create_unsigned_txs(from_address, to_address, amount, file_name):
    try:
        status, unsignedTx = tx_send(
            from_address,
            to_address,
            amount,
            gas=DEFAULT_GAS,
            unsigned=True,
        )
        if not status:
            return status, unsignedTx
        with open(f"{HOME}/{file_name}", "w") as outfile:
            json.dump(unsignedTx, outfile)
        return True, unsignedTx
    except Exception as e:
        return False, e


# 'sign_and_broadcast_txs' takes unsigned_file, signed_file, from_address and sequence as parameters.
# Signs and the broadcasts the unsigned transactions.
def sign_and_broadcast_txs(unsigned_file, signed_file, from_address, sequence):
    try:
        status, signTx = tx_sign(unsigned_file, from_address, sequence, DEFAULT_GAS)
        if not status:
            return status, signTx
        with open(f"{HOME}/{signed_file}", "w") as outfile:
            json.dump(signTx, outfile)

        status, broadcast_response = tx_broadcast(signed_file, DEFAULT_GAS, "block")
        if not status:
            return status, broadcast_response
        return status, broadcast_response["txhash"]
    except Exception as e:
        return False, e


# tx_send takes from_address, to_address and amount as paramaters and
# internally calls the 'tx send' command and return the response in json format.
def tx_send(
    from_address,
    to_address,
    amount,
    gas=DEFAULT_GAS,
    unsigned=False,
    sequence=None,
):
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
            elif Tx["code"] != 0:
                return False, Tx
            return True, Tx
    except Exception as e:
        return False, e
