import argparse, os
import json
import sys
from core.keys import keys_show
from modules.auth.query import query_account
from modules.bank.tx import tx_send
from utils.commands import exec_command
from utils.types import account_type

# import env values
DAEMON = os.getenv('DAEMON')
DENOM = os.getenv('DENOM')
CHAINID = os.getenv('CHAINID')
DAEMON_HOME = os.getenv('DAEMON_HOME')

parser = argparse.ArgumentParser(description='This program takes inputs for intializing multi message load test.')
parser.add_argument('-s', '--sender', type= account_type, default = keys_show("account1")[1]['address'],help= 'From which account the transaction should be intialized')
parser.add_argument('-r','reciever', type= account_type, default = keys_show("account1")[1]['address'], help= 'Reciever account number.')
args = parser.parse_args()

acc1, acc2 = args.sender, args.reciever

# query account sequence
status, account = query_account(acc1)
if not status:
    sys.exit(account)
seq1no = int(account['sequence'])
bound = 10000 + seq1no
print(f"seq1no : {seq1no}")

for i in range(seq1no, bound):
    status, sTx = tx_send(acc1, acc2, 1000000, 200000, sequence= i)
    if not status:
        print(sTx)
    else:
        sTxHash=sTx['txhash']
        print(f"** TX HASH :: {sTxHash} **")
