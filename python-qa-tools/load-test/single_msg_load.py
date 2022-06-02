import argparse, os, sys, time, logging
from core.keys import keys_show
from modules.auth.query import account_type, query_account
from modules.bank.query import query_balances
from modules.bank.tx import tx_send
from utils import num_txs_type, print_balance_deductions

HOME = os.getenv('HOME')
logging.basicConfig(format='%(message)s',
                    level=logging.DEBUG)

parser = argparse.ArgumentParser(description='This program takes inputs for intializing multi message load test.')
parser.add_argument('-s', '--sender', type = account_type, default = keys_show("account1")[1]['address'], help = 'Sender bech32 address')
parser.add_argument('-r', '--receiver', type= account_type, default = keys_show("account2")[1]['address'], help= 'Receiver bech32 address')
parser.add_argument('-n', '--num_txs', type = num_txs_type, default = 10000, help= 'Number of transactions to be made, atleast should be 1000')
args = parser.parse_args()
sender, receiver, NUM_TXS, amount_to_be_sent = args.sender, args.receiver, int(args.num_txs), 1000000

if sender == receiver:
    sys.exit('Error: The values of arguments "sender" and "receiver" are equal make sure to set different values')


#### Fetch Balances from sender receiver ####
status, sender_balance_old= query_balances(sender)
if not status:
    sys.exit(sender_balance_old)
sender_balance_old = sender_balance_old['balances'][0]['amount']

status, receiver_balance_old = query_balances(receiver)
if not status:
    sys.exit(receiver_balance_old)
receiver_balance_old = receiver_balance_old['balances'][0]['amount']

#### Fetching sequence numbers of to and from accounts
os.chdir(os.path.expanduser(HOME))
status, seq1_response = query_account(sender)
if not status:
    sys.exit(seq1_response)

status, seq2_response = query_account(receiver)
if not status:
    sys.exit(seq2_response)

seq1no, seq2no = int(seq1_response['sequence']), int(seq2_response['sequence'])

for i in range(NUM_TXS):
    seqto = seq1no + i
    seqfrom = seq2no + i
    status, sTxto = tx_send(sender, receiver, amount_to_be_sent, None, False, seqto)
    if not status:
        logging.error(f"{sTxto}")
    else:
        logging.info(f"TX HASH to :: {sTxto['txhash']}")
    
    status, sTxfrom = tx_send(receiver, sender, amount_to_be_sent , None, False, seqfrom)
    if not status:
        logging.error(f"{sTxfrom}")
    else:
        logging.info(f"TX HASH from :: {sTxto['txhash']}")

logging.info('waiting for tx confirmation, avg time is 7s.')
time.sleep(7)

#### Print Balances ####
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
