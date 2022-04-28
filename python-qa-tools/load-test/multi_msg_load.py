import argparse, os, sys, json, time
from utils.bank import balance_query, print_balance_deductions
from utils.commands import command_processor
from utils.keys import fetch_account_address
from utils.txs import fetch_seq_no, signed_tx, unsigned_tx, write_json
from utils.types import account_type, num_txs_type

DAEMON = os.getenv('DAEMON')
DENOM = os.getenv('DENOM')
CHAINID = os.getenv('CHAINID')
DAEMON_HOME = os.getenv('DAEMON_HOME')
HOME = os.getenv('HOME')

parser = argparse.ArgumentParser(description='This program takes inputs for intializing multi message load test.')
parser.add_argument('FROM', type= account_type, help= 'From which account the transaction should be intialized')
parser.add_argument('TO', type= account_type, help= 'Reciever account number.')
parser.add_argument('NUM_TXS', type = num_txs_type, help= 'Number of transactions to be made, Min. should be 1000')

args = parser.parse_args()
FROM, TO, NUM_TXS = int(args.FROM), int(args.TO), int(args.NUM_TXS)

if FROM == TO:
    sys.exit('Error: The values of arguments "TO" and "FROM" are equal make sure to set different values')

RPC, num_msgs = "http://127.0.0.1:16657", 30

#### Fetching Bech addresses ######
acc1, acc1err = fetch_account_address(f"account{FROM}")
if len(acc1err):
    sys.exit(acc1err)

acc2, acc2err = fetch_account_address(f"account{TO}")
if len(acc2err):
    sys.exit(acc2err)

#### Fetch Balances from acc1 acc2 ####
before_acc1_balance, before_acc1_balanceerr = balance_query(acc1, RPC)
if len(before_acc1_balanceerr):
    sys.exit(before_acc1_balanceerr)

before_acc2_balance, before_acc2_balanceerr = balance_query(acc2, RPC)
if len(before_acc2_balanceerr):
    sys.exit(before_acc2_balanceerr)

#### Sequences ####
os.chdir(os.path.expanduser(HOME))
status, seq1no = fetch_seq_no(acc1, RPC)
if not status:
    sys.exit(seq1no)

status, seq2no = fetch_seq_no(acc2, RPC)
if not status:
    sys.exit(seq2no)

for i in range(0, int(NUM_TXS)):
    status, unsignedTxto = unsigned_tx(acc1, acc2, 'unsignedto.json')
    if not status:
        print(unsignedTxto)
    
    status, unsignedTxfrom = unsigned_tx(acc2, acc1, 'unsignedfrom.json')
    if not status:
        print(unsignedTxfrom)
        
    for j in range(0, int(num_msgs)):
        write_json('unsignedto.json')
        write_json('unsignedfrom.json')

    ### seqto ###
    seqto = seq1no + i
    status, txHash = signed_tx('unsignedto.json', 'signedto.json', acc1, seqto, RPC)
    if not status:
        print(txHash)
    else:
        print(f"broadcasttoTxhash: {txHash}")

    ### seqfrom ###
    seqfrom = seq2no + i
    status, txHash = signed_tx('unsignedfrom.json', 'signedfrom.json', acc2, seqfrom, RPC)
    if not status:
        print(txHash)
    else:
        print(f"broadcastfromTxhash: {txHash}")

print('##### Sleeping for 7s #####')
time.sleep(7)

#### Print Balances ####
after_acc1_balance, after_acc1_balanceerr = balance_query(acc1, RPC)
if len(after_acc1_balanceerr):
    sys.exit(after_acc1_balanceerr)

after_acc2_balance, after_acc2_balanceerr = balance_query(acc2, RPC)
if len(after_acc2_balanceerr):
    sys.exit(after_acc2_balanceerr)

acc1_diff = int(before_acc1_balance) - int(after_acc1_balance)
acc2_diff = int(before_acc2_balance) - int(after_acc2_balance)

print_balance_deductions('account1', acc1_diff)
print_balance_deductions('account2', acc2_diff)
