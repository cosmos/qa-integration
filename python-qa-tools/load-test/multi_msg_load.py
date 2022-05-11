import argparse, os, sys, time
import logging
from core.keys import keys_show
from modules.auth.query import query_account
from modules.bank.query import query_balances
from utils.bank import print_balance_deductions
from utils.txs import signed_tx, unsigned_tx, write_json
from utils.types import account_type, num_txs_type

CHAINID = os.getenv('CHAINID')
DAEMON = os.getenv('DAEMON')
DAEMON_HOME = os.getenv('DAEMON_HOME')
DENOM = os.getenv('DENOM')
HOME = os.getenv('HOME')

parser = argparse.ArgumentParser(description='This program takes inputs for intializing multi message load test.')
parser.add_argument('-s', '--sender', type = account_type, default = keys_show("account1")[1]['address'], help = 'Sender bech32 address')
parser.add_argument('-r', '--reciever', type= account_type, default = keys_show("account2")[1]['address'], help= 'Reciever bech32 address')
parser.add_argument('-n', '--num_txs', type = num_txs_type, default = 1000, help= 'Number of transactions to be made, Min. should be 1000')
args = parser.parse_args()
FROM, TO, NUM_TXS = args.sender, args.reciever, int(args.num_txs)

if FROM == TO:
    sys.exit('Error: The values of arguments "TO" and "FROM" are equal make sure to set different values')
 
acc1, acc2, num_msgs = FROM, TO, 30

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
for i in range(0, int(NUM_TXS)):
    status, unsignedTxto = unsigned_tx(acc1, acc2, 'unsignedto.json')
    if not status:
        print(unsignedTxto)
    
    status, unsignedTxfrom = unsigned_tx(acc2, acc1, 'unsignedfrom.json')
    if not status:
        print(unsignedTxfrom)
#### Duplicating and appending transfer message in the existing array to create a multi-msg transaction        
    for j in range(0, int(num_msgs)):
        write_json('unsignedto.json')
        write_json('unsignedfrom.json')

    ### Signing and broadcasting the unsigned transactions from acc1 to acc2 ###
    seqto = seq1no + i
    status, txHash = signed_tx('unsignedto.json', 'signedto.json', acc1, seqto)
    if not status:
        print(txHash)
    else:
        print(f"broadcasttoTxhash: {txHash}")

    ### Signing and broadcasting the unsigned transactions from acc2 to acc1 ###
    seqfrom = seq2no + i
    status, txHash = signed_tx('unsignedfrom.json', 'signedfrom.json', acc2, seqfrom)
    if not status:
        print(txHash)
    else:
        print(f"broadcastfromTxhash: {txHash}")

print('##### Sleeping for 7s #####')
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
