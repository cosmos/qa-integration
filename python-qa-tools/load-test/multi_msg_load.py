import argparse, os, sys, time
import logging
from core.keys import keys_show
from modules.auth.query import query_account
from modules.bank.query import query_balances
from utils.bank import print_balance_deductions
from utils.txs import create_signed_txs, create_unsigned_txs, create_multi_messages
from utils.types import account_type

CHAINID = os.getenv('CHAINID')
DAEMON = os.getenv('DAEMON')
DAEMON_HOME = os.getenv('DAEMON_HOME')
DENOM = os.getenv('DENOM')
HOME = os.getenv('HOME')
NUM_MSGS = os.getenv('NUM_MSGS')
logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

parser = argparse.ArgumentParser(description='This program takes inputs for intializing multi message load test.')
parser.add_argument('-s', '--sender', type = account_type, default = keys_show("account1")[1]['address'], help = 'Sender bech32 address')
parser.add_argument('-r', '--receiver', type= account_type, default = keys_show("account2")[1]['address'], help= 'Receiver bech32 address')
parser.add_argument('-n', '--num_txs', type = int, default = 1000, help= 'Number of transactions to be made, atleast should be 1000')
args = parser.parse_args()
FROM, TO, NUM_TXS = args.sender, args.receiver, int(args.num_txs)

if FROM == TO:
    sys.exit('Error: The values of arguments "TO" and "FROM" are equal make sure to set different values')
 
acc1, acc2, num_msgs = FROM, TO, NUM_MSGS

#### Fetch Balances of acc1 acc2 before execting the load test ####
status, before_acc1_balance= query_balances(acc1)
if not status:
    sys.exit(before_acc1_balance)
before_acc1_balance = before_acc1_balance['balances'][0]['amount']

status, before_acc2_balance = query_balances(acc2)
if not status:
    sys.exit(before_acc2_balance)
before_acc2_balance = before_acc2_balance['balances'][0]['amount']

#### Fetching sequence numbers of to and from accounts
os.chdir(os.path.expanduser(HOME))
status, seq1_response = query_account(acc1)
if not status:
    sys.exit(seq1_response)

status, seq2_response = query_account(acc2)
if not status:
    sys.exit(seq2_response)

seq1no, seq2no = int(seq1_response['sequence']), int(seq2_response['sequence'])    


#### Generating unsigned transactions with a single transfer message 
for i in range(NUM_TXS):
    status, unsignedTxto = create_unsigned_txs(acc1, acc2, 'unsignedto.json')
    if not status:
        logging.error(unsignedTxto)
    
    status, unsignedTxfrom = create_unsigned_txs(acc2, acc1, 'unsignedfrom.json')
    if not status:
        logging.error(unsignedTxfrom)
        
#### Duplicating and appending transfer message in the existing array to create a multi-msg transaction        
    for j in range(num_msgs):
        create_multi_messages('unsignedto.json')
        create_multi_messages('unsignedfrom.json')

    ### Signing and broadcasting the unsigned transactions from acc1 to acc2 ###
    seqto = seq1no + i
    status, txHash = create_signed_txs('unsignedto.json', 'signedto.json', acc1, seqto)
    if not status:
        logging.error(f"sign_and_broadcast_tx failed : {txHash}")
    else:
        logging.info(f"broadcasttoTxhash: {txHash}")

    ### Signing and broadcasting the unsigned transactions from acc2 to acc1 ###
    seqfrom = seq2no + i
    status, txHash = create_signed_txs('unsignedfrom.json', 'signedfrom.json', acc2, seqfrom)
    if not status:
        logging.error(f"sign_and_broadcast_tx failed : {txHash}")
    else:
        logging.info(f"broadcastfromTxhash: {txHash}")

logging.info('waiting for tx confirmation, avg time is 7s.')
time.sleep(7)

#### Verifying the balance deductions ####
status, after_acc1_balance = query_balances(acc1)
if not status:
    sys.exit(after_acc1_balance)
after_acc1_balance = after_acc1_balance['balances'][0]['amount']

status, after_acc2_balance = query_balances(acc2)
if not status:
    sys.exit(after_acc2_balance)
after_acc2_balance = after_acc2_balance['balances'][0]['amount']

acc1_diff = int(before_acc1_balance) - int(after_acc1_balance)
acc2_diff = int(before_acc2_balance) - int(after_acc2_balance)

print_balance_deductions('account1', acc1_diff)
print_balance_deductions('account2', acc2_diff)
