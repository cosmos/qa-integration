"""
This script test a series of bank transfer transactions with multiple messages between two accounts.
It takes two optional arguments namely -s(sender) and -r(receiver)
"""
import argparse
import os
import sys
import time
import logging
from core.keys import keys_show
from modules.auth.query import account_type, query_account
from modules.bank.query import query_balances
from modules.bank.tx import sign_and_broadcast_txs, create_unsigned_txs
from utils import create_multi_messages, validate_num_txs, print_balance_deductions

HOME = os.getenv("HOME")
NUM_MSGS = int(os.getenv("NUM_MSGS"))
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

parser = argparse.ArgumentParser(
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
    default=1000,
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

# Fetch balances of sender and receiver accounts before executing the load test
status, sender_bal_after = query_balances(sender)
if not status:
    sys.exit(sender_bal_after)
sender_bal_after = int(sender_bal_after["balances"][0]["amount"])

# Fetch Balances of receiver executing the load test
status, receiver_bal_before = query_balances(receiver)
if not status:
    sys.exit(receiver_bal_before)
receiver_bal_before = int(receiver_bal_before["balances"][0]["amount"])

# Fetching sequence numbers of to and from accounts
status, sender_acc = query_account(sender)
if not status:
    sys.exit(sender_acc)

status, receiver_acc = query_account(receiver)
if not status:
    sys.exit(receiver_acc)

sender_acc_seq, receiver_acc_seq = int(sender_acc["sequence"]), int(
    receiver_acc["sequence"]
)

# Generating unsigned transactions with a single transfer message
status, unsigned_tx_to = create_unsigned_txs(
    sender, receiver, amount, "unsignedto.json"
)
if not status:
    logging.error(unsigned_tx_to)

status, unsigned_tx_from = create_unsigned_txs(
    receiver, sender, amount, "unsignedfrom.json"
)
if not status:
    logging.error(unsigned_tx_from)

for i in range(num_txs):

    # Duplicating and appending transfer message in the existing array
    # to create a multi-msg transaction.
    create_multi_messages(NUM_MSGS, "unsignedto.json")
    create_multi_messages(NUM_MSGS, "unsignedfrom.json")

    # Signing and broadcasting the unsigned transactions from sender to receiver
    seqto = sender_acc_seq + i
    status, tx_hash = sign_and_broadcast_txs(
        "unsignedto.json", "signedto.json", sender, seqto
    )
    if not status:
        logging.error(
            "sign_and_broadcast_tx from sender to receiver failed : %s", tx_hash
        )
    else:
        logging.info("broadcasted tx_hash: %s", tx_hash)

    # Signing and broadcasting the unsigned transactions from receiver to sender
    seqfrom = receiver_acc_seq + i
    status, tx_hash = sign_and_broadcast_txs(
        "unsignedfrom.json", "signedfrom.json", receiver, seqfrom
    )
    if not status:  # if the txn is unsuccessful
        logging.error(
            "sign_and_broadcast_tx from receiver to sender failed : %s", tx_hash
        )
    else:
        logging.info("broadcasted tx_hash: %s", tx_hash)

logging.info("waiting for tx confirmation, avg time is 7s.")
time.sleep(7)

# Verifying the balance deductions
status, sender_bal_after = query_balances(sender)
if not status:
    sys.exit(sender_bal_after)
sender_bal_after = sender_bal_after["balances"][0]["amount"]

status, receiver_bal_after = query_balances(receiver)
if not status:
    sys.exit(receiver_bal_after)
receiver_bal_after = receiver_bal_after["balances"][0]["amount"]

sender_diff = int(sender_bal_after) - int(sender_bal_after)
receiver_diff = int(receiver_bal_before) - int(receiver_bal_after)

print_balance_deductions("sender", sender_diff)
print_balance_deductions("receiver", receiver_diff)
