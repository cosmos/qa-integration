"""
This script test a series of bank transfer transactions with single message between two accounts.
It takes two optional arguments namely -s(sender) and -r(receiver).
"""
import argparse
import os
import sys
import time
import logging
from core.keys import keys_show
from modules.auth.query import account_type, query_account
from modules.bank.query import query_balances
from modules.bank.tx import tx_send
from utils import validate_num_txs, print_balance_deductions

HOME = os.getenv("HOME")
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

parser = argparse.ArgumentpParser(
    description="This program takes inputs for intializing multi message load test."
)
parser.add_argument(
    "-s",
    "--sender",
    type=account_type,
    default=keys_show("account1")[1]["address"],
    help="sender bech32 address",
)
parser.add_argument(
    "-r",
    "--receiver",
    type=account_type,
    default=keys_show("account2")[1]["address"],
    help="receiver bech32 address",
)
parser.add_argument(
    "-n",
    "--num_txs",
    type=validate_num_txs,
    default=10000,
    help="Number of transactions to be made, should be positive integer",
)
args = parser.parse_args()
sender = args.sender
receiver = args.receiver
num_txs = int(args.num_txs)
amount = 1000000

if sender == receiver:
    sys.exit(
        """Error: The values of arguments "sender" and "receiver"
             are equal make sure to set different values"""
    )

#### Fetch Balances from sender receiver ####
status, sender_bal_old = query_balances(sender)
if not status:
    sys.exit(sender_bal_old)
sender_bal_old = sender_bal_old["balances"][0]["amount"]

status, receiver_bal_old = query_balances(receiver)
if not status:
    sys.exit(receiver_bal_old)
receiver_bal_old = receiver_bal_old["balances"][0]["amount"]

# Fetching sequence numbers of to and from accounts
os.chdir(os.path.expanduser(HOME))
status, sender_acc = query_account(sender)
if not status:
    sys.exit(sender_acc)

status, receiver_acc = query_account(receiver)
if not status:
    sys.exit(receiver_acc)

sender_acc_seq, receiver_acc_seq = int(sender_acc["sequence"]), int(
    receiver_acc["sequence"]
)

for i in range(num_txs):
    seqto = sender_acc_seq + i
    seqfrom = receiver_acc_seq + i
    status, stx_to = tx_send(sender, receiver, amount, 100000, False, seqto)
    if not status:
        logging.error("%s", stx_to)
    else:
        logging.info("TX HASH to :: %s", stx_to["txhash"])
    status, stx_from = tx_send(receiver, sender, amount, 100000, False, seqfrom)
    if not status:
        logging.error("%s", stx_from)
    else:
        logging.info("TX HASH from :: %s", stx_to["txhash"])

logging.info("waiting for tx confirmation, avg time is 7s.")
time.sleep(7)

#### Print Balances ####
status, sender_bal_updated = query_balances(sender)
if not status:
    sys.exit(sender_bal_updated)
sender_bal_updated = sender_bal_updated["balances"][0]["amount"]

status, receiver_bal_updated = query_balances(receiver)
if not status:
    sys.exit(receiver_bal_updated)
receiver_bal_updated = receiver_bal_updated["balances"][0]["amount"]

sender_diff = int(sender_bal_old) - int(sender_bal_updated)
receiver_diff = int(receiver_bal_old) - int(receiver_bal_updated)

print_balance_deductions("sender", sender_diff)
print_balance_deductions("receiver", receiver_diff)
