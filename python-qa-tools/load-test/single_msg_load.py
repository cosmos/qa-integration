import argparse, os, sys, json, time
from utils.bank import balance_query, print_balance_deductions
from utils.commands import command_processor
from utils.keys import fetch_account_address
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

RPC = "http://127.0.0.1:16657"

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
command = f"{DAEMON} q account {acc1} --node {RPC} --output json"
seq1, seq1err = command_processor(command)
seq1 = json.loads(seq1)
if len(seq1err):
    sys.exit(seq1err)
seq1no = int(seq1['sequence'])

command = f"{DAEMON} q account {acc2} --node {RPC} --output json"
seq2, seq2err = command_processor(command)
if len(seq2err):
    sys.exit(seq2err)
seq2 = json.loads(seq2)
seq2no = int(seq2['sequence'])

for i in range(0, NUM_TXS):
    seqto = seq1no + i
    seqfrom = seq2no + i
    sTxto= f"{DAEMON} tx bank send {acc1} {acc2} 1000000{DENOM} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --sequence {seqto}" 
    sTxto, sTxtoerr = command_processor(sTxto)
    if len(sTxtoerr):
        sys.exit(sTxtoerr)
    sTxto = json.loads(sTxto)
    print(f"** TX HASH :: {sTxto['txhash']} **")
    
    sTxfrom = f"{DAEMON} tx bank send {acc2} {acc1} 1000000{DENOM} --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} --output json -y --sequence {seqfrom}"
    sTxfrom, sTxfromerr = command_processor(sTxfrom)
    if len(sTxfromerr):
        sys.exit(sTxfromerr)
    sTxfrom = json.loads(sTxfrom)
    print(f"** TX HASH :: {sTxfrom['txhash']} **")

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
