import argparse, os
import json
import sys
from utils.bank import query_account
from utils.commands import command_processor
from utils.keys import fetch_account_address
from utils.types import account_type

# import env values
DAEMON = os.getenv('DAEMON')
DENOM = os.getenv('DENOM')
CHAINID = os.getenv('CHAINID')
DAEMON_HOME = os.getenv('DAEMON_HOME')

parser = argparse.ArgumentParser(description='This program takes inputs for intializing multi message load test.')
parser.add_argument('FROM', type= account_type, help= 'From which account the transaction should be intialized')
parser.add_argument('TO', type= account_type, help= 'Reciever account number.')
args = parser.parse_args()

FROM = int(args.FROM)
TO = int(args.TO)

IP = "127.0.0.1"
PORT = "16657"

RPC = f"http://{IP}:{PORT}"

# Fetch account1 address
acc1, acc1err = fetch_account_address(f"account{FROM}")
if len(acc1err):
    sys.exit(acc1err)

# Fetch account2 address
acc2, acc2err = fetch_account_address(f"account{TO}")
if len(acc2err):
    sys.exit(acc2err)

# query account sequence
seq1, seq1err = query_account(acc1, RPC)
if len(seq1err):
    sys.exit(seq1err)
seq1no = int(seq1['sequence'])
bound = 10000 + seq1no
print(f"seq1no : {seq1no}")
for i in range(seq1no, bound):
    sTxcommad = f"{DAEMON} tx bank send {acc1} {acc2} 1000000{DENOM} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --sequence {i}"
    sTx, sTxerr = command_processor(sTxcommad)
    if len(sTxerr):
        print(f"sTxerr : {sTxerr}")
    sTx = json.loads(sTx)
    sTxHash=sTx['txhash']
    print(f"** TX HASH :: {sTxHash} **")
