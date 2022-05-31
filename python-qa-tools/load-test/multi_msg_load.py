import argparse, os, sys, time
import logging
from core.keys import keys_show
from modules.auth.query import account_type, query_account
from modules.bank.query import query_balances
from modules.bank.tx import create_signed_txs, create_unsigned_txs
from utils import create_multi_messages, print_balance_deductions

HOME = os.getenv('HOME')
NUM_MSGS = int(os.getenv('NUM_MSGS'))
 
logging.basicConfig(format='%(message)s',
                    level=logging.DEBUG)

parser = argparse.ArgumentParser(description='This program takes inputs for intializing multi message load test.')
parser.add_argument('-s', '--sender', type = account_type, default = keys_show("account1")[1]['address'], help = 'Sender bech32 address')
parser.add_argument('-r', '--receiver', type= account_type, default = keys_show("account2")[1]['address'], help= 'Receiver bech32 address')
parser.add_argument('-n', '--num_txs', type = int, default = 1000, help= 'Number of transactions to be made, atleast should be 1000')
args = parser.parse_args()
FROM, TO, NUM_TXS = args.sender, args.receiver, int(args.num_txs)

if FROM == TO:
    sys.exit('Error: The values of arguments "TO" and "FROM" are equal make sure to set different values')
 
sender, receiver, num_msgs = FROM, TO, NUM_MSGS

#### Fetch Balances of sender receiver before execting the load test ####
status, before_sender_balance= query_balances(sender)
if not status:
    sys.exit(before_sender_balance)
before_sender_balance = before_sender_balance['balances'][0]['amount']

status, before_receiver_balance = query_balances(receiver)
if not status:
    sys.exit(before_receiver_balance)
before_receiver_balance = before_receiver_balance['balances'][0]['amount']

#### Fetching sequence numbers of to and from accounts
os.chdir(os.path.expanduser(HOME))
status, seq1_response = query_account(sender)
if not status:
    sys.exit(seq1_response)

status, seq2_response = query_account(receiver)
if not status:
    sys.exit(seq2_response)

seq1no, seq2no = int(seq1_response['sequence']), int(seq2_response['sequence'])    


#### Generating unsigned transactions with a single transfer message 
for i in range(NUM_TXS):
    status, unsignedTxto = create_unsigned_txs(sender, receiver, 'unsignedto.json')
    if not status:
        logging.error(unsignedTxto)
    
    status, unsignedTxfrom = create_unsigned_txs(receiver, sender, 'unsignedfrom.json')
    if not status:
        logging.error(unsignedTxfrom)
        
#### Duplicating and appending transfer message in the existing array to create a multi-msg transaction        
    for j in range(num_msgs):
        create_multi_messages('unsignedto.json')
        create_multi_messages('unsignedfrom.json')

    ### Signing and broadcasting the unsigned transactions from sender to receiver ###
    seqto = seq1no + i
    status, txHash = create_signed_txs('unsignedto.json', 'signedto.json', sender, seqto)
    if not status:
        logging.error(f"sign_and_broadcast_tx to failed : {txHash}")
    else:
        logging.info(f"broadcasttoTxhash: {txHash}")

    ### Signing and broadcasting the unsigned transactions from receiver to sender ###
    seqfrom = seq2no + i
    status, txHash = create_signed_txs('unsignedfrom.json', 'signedfrom.json', receiver, seqfrom)
    if not status:
        logging.error(f"sign_and_broadcast_tx from failed : {txHash}")
    else:
        logging.info(f"broadcastfromTxhash: {txHash}")

logging.info('waiting for tx confirmation, avg time is 7s.')
time.sleep(7)

#### Verifying the balance deductions ####
status, after_sender_balance = query_balances(sender)
if not status:
    sys.exit(after_sender_balance)
after_sender_balance = after_sender_balance['balances'][0]['amount']

status, after_receiver_balance = query_balances(receiver)
if not status:
    sys.exit(after_receiver_balance)
after_receiver_balance = after_receiver_balance['balances'][0]['amount']

sender_diff = int(before_sender_balance) - int(after_sender_balance)
receiver_diff = int(before_receiver_balance) - int(after_receiver_balance)

print_balance_deductions('account1', sender_diff)
print_balance_deductions('account2', receiver_diff)
