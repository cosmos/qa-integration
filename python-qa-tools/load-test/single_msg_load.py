import argparse, os, sys, time
from core.keys import keys_show
from modules.auth.query import query_account
from modules.bank.query import query_balances
from modules.bank.tx import tx_send
from utils.bank import print_balance_deductions
from utils.types import account_type, num_txs_type


CHAINID = os.getenv('CHAINID')
DAEMON = os.getenv('DAEMON')
DAEMON_HOME = os.getenv('DAEMON_HOME')
DENOM = os.getenv('DENOM')
HOME = os.getenv('HOME')

parser = argparse.ArgumentParser(description='This program takes inputs for intializing multi message load test.')
parser.add_argument('-s', '--sender', type = account_type, default = keys_show("account1")[1]['address'], help = 'Sender bech32 address')
parser.add_argument('-r', '--reciever', type= account_type, default = keys_show("account2")[1]['address'], help= 'Reciever bech32 address')
parser.add_argument('-n', '--num_txs', type = num_txs_type, default = 10000, help= 'Number of transactions to be made, Min. should be 1000')
args = parser.parse_args()
FROM, TO, NUM_TXS = args.sender, args.reciever, int(args.num_txs)

if FROM == TO:
    sys.exit('Error: The values of arguments "TO" and "FROM" are equal make sure to set different values')
 
acc1, acc2 = FROM, TO

#### Fetch Balances from acc1 acc2 ####
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

for i in range(NUM_TXS):
    seqto = seq1no + i
    seqfrom = seq2no + i
    status, sTxto = tx_send(acc1, acc2, 1000000, None, False, seqto)
    if not status:
        print(f"Error : {sTxto}")
    else:
        print(f"** TX HASH to :: {sTxto['txhash']} **")
    
    status, sTxfrom = tx_send(acc2, acc1, 1000000, None, False, seqfrom)
    if not status:
        print(f"Error : {sTxfrom}")
    else:
        print(f"** TX HASH to :: {sTxto['txhash']} **")

print('##### Sleeping for 7s #####')
time.sleep(7)

#### Print Balances ####
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
