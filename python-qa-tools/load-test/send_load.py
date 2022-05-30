import argparse, os,sys, logging
from core.keys import keys_show
from modules.auth.query import query_account
from modules.bank.tx import tx_send
from utils.types import account_type

# import env values
logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

parser = argparse.ArgumentParser(description='This program takes inputs for intializing multi message load test.')
parser.add_argument('-s', '--sender', type= account_type, default = keys_show("account1")[1]['address'],help= 'From which account the transaction should be intialized')
parser.add_argument('-r','--receiver', type= account_type, default = keys_show("account1")[1]['address'], help= 'Receiver account number.')
args = parser.parse_args()

sender, receiver = args.sender, args.receiver

# query account sequence
status, account = query_account(sender)
if not status:
    sys.exit(account)
seq1no = int(account['sequence'])
bound = 10000 + seq1no
logging.info(f"seq1no : {seq1no}")

for i in range(seq1no, bound):
    status, sTx = tx_send(sender, receiver, 1000000, 200000, sequence= i)
    if not status:
        logging.error(sTx)
    else:
        sTxHash=sTx['txhash']
        logging.info(f"TX HASH :: {sTxHash}")
