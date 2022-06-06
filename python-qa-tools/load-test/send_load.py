import argparse, os,sys, logging
from core.keys import keys_show
from modules.auth.query import account_type, query_account
from modules.bank.tx import tx_send

logging.basicConfig(format='%(message)s',
                    level=logging.DEBUG)

parser = argparse.ArgumentParser(description='This program takes inputs for intializing multi message load test.')
parser.add_argument('-s', '--sender', type= account_type, default = keys_show("account1")[1]['address'],help= 'From which account the transaction should be intialized')
parser.add_argument('-r','--receiver', type= account_type, default = keys_show("account2")[1]['address'], help= 'Receiver account number.')
args = parser.parse_args()

sender, receiver = args.sender, args.receiver

# query account sequence
status, account = query_account(sender)
if not status:
    sys.exit(account)
seq1no = int(account['sequence'])
bound = 10000 + seq1no
logging.info(f"initial sequence number of sender account : {seq1no}")

for i in range(seq1no, bound):
    status, tx = tx_send(sender, receiver, 1000000, 200000, sequence= i)
    if not status:
        logging.error(tx)
    else:
        txhash=tx['txhash']
        logging.info(f"TX HASH :: {txhash}")
