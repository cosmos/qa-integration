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
sender, receiver, NUM_TXS, amount_to_be_sent = args.sender, args.receiver, int(args.num_txs), 1000000

if sender == receiver:
    sys.exit('Error: The values of arguments "sender" and "receiver" are equal make sure to set different values')


#### Fetch balances of sender and receiver accounts before executing the load test ####
status, sender_balance_old= query_balances(sender)
if not status:
    sys.exit(sender_balance_old)
sender_balance_old = int(sender_balance_old['balances'][0]['amount'])

#### Fetch Balances of receiver executing the load test ####
status, receiver_balance_old = query_balances(receiver)
if not status:
    sys.exit(receiver_balance_old)
receiver_balance_old = int(receiver_balance_old['balances'][0]['amount'])

### Fetch Sender's expected balance after load test #####
sender_expected_balance = sender_balance_old - amount_to_be_sent    
### Fetch Receiver's expected balance after load test###


#### Fetching sequence numbers of to and from accounts
status, seq1_response = query_account(sender)
if not status:
    sys.exit(seq1_response)

status, seq2_response = query_account(receiver)
if not status:
    sys.exit(seq2_response)

seq1no, seq2no = int(seq1_response['sequence']), int(seq2_response['sequence'])    


#### Generating unsigned transactions with a single transfer message 
status, unsignedTxto = create_unsigned_txs(sender, receiver, amount_to_be_sent, 'unsignedto.json')
if not status:
    logging.error(unsignedTxto)

status, unsignedTxfrom = create_unsigned_txs(receiver, sender, amount_to_be_sent, 'unsignedfrom.json')
if not status:
    logging.error(unsignedTxfrom)
        
for i in range(NUM_TXS):
        
#### Duplicating and appending transfer message in the existing array to create a multi-msg transaction        
    create_multi_messages(NUM_MSGS, 'unsignedto.json')
    create_multi_messages(NUM_MSGS, 'unsignedfrom.json')

    ### Signing and broadcasting the unsigned transactions from sender to receiver ###
    seqto = seq1no + i
    status, txHash = create_signed_txs('unsignedto.json', 'signedto.json', sender, seqto)
    if not status:
        logging.error(f"sign_and_broadcast_tx from sender to receiver failed : {txHash}")
    else:
        logging.info(f"broadcasted txhash: {txHash}")

    ### Signing and broadcasting the unsigned transactions from receiver to sender ###
    seqfrom = seq2no + i
    status, txHash = create_signed_txs('unsignedfrom.json', 'signedfrom.json', receiver, seqfrom)
    if not status: # if the txn is unsuccessful
        logging.error(f"sign_and_broadcast_tx from receiver to sender failed : {txHash}")
    else:
        logging.info(f"broadcasted txhash: {txHash}")

logging.info('waiting for tx confirmation, avg time is 7s.')
time.sleep(7)

#### Verifying the balance deductions ####
status, sender_balance_updated = query_balances(sender)
if not status:
    sys.exit(sender_balance_updated)
sender_balance_updated = sender_balance_updated['balances'][0]['amount']

status, receiver_balance_updated = query_balances(receiver)
if not status:
    sys.exit(receiver_balance_updated)
receiver_balance_updated = receiver_balance_updated['balances'][0]['amount']

sender_diff = int(sender_balance_old) - int(sender_balance_updated)
receiver_diff = int(receiver_balance_old) - int(receiver_balance_updated)

print_balance_deductions('sender', sender_diff)
print_balance_deductions('receiver', receiver_diff)

