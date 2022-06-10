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

PARSER = argparse.ArgumentParser(
    description="This program takes inputs for intializing multi message load test."
)
PARSER.add_argument(
    "-s",
    "--sender",
    type=account_type,
    default=keys_show("account1")[1]["address"],
    help="Sender bech32 address",
)
PARSER.add_argument(
    "-r",
    "--receiver",
    type=account_type,
    default=keys_show("account2")[1]["address"],
    help="Receiver bech32 address",
)
PARSER.add_argument(
    "-n",
    "--num_txs",
    type=validate_num_txs,
    default=1000,
    help="Number of transactions to be made, should be positive integer",
)
ARGS = PARSER.parse_args()
SENDER = ARGS.sender
RECEIVER = ARGS.receiver
NUM_TXS = int(ARGS.num_txs)
AMOUNT = 1000000

if SENDER == RECEIVER:
    sys.exit(
        """Error: The values of arguments "sender" and "receiver"
            are equal make sure to set different values"""
    )

# Fetch balances of sender and receiver accounts before executing the load test
STATUS, SENDER_BAL_AFTER = query_balances(SENDER)
if not STATUS:
    sys.exit(SENDER_BAL_AFTER)
SENDER_BAL_AFTER = int(SENDER_BAL_AFTER["balances"][0]["amount"])

# Fetch Balances of receiver executing the load test
STATUS, RECEIVER_BAL_BEFORE = query_balances(RECEIVER)
if not STATUS:
    sys.exit(RECEIVER_BAL_BEFORE)
RECEIVER_BAL_BEFORE = int(RECEIVER_BAL_BEFORE["balances"][0]["amount"])

# Fetching sequence numbers of to and from accounts
STATUS, SENDER_ACC = query_account(SENDER)
if not STATUS:
    sys.exit(SENDER_ACC)

STATUS, RECEIVER_ACC = query_account(RECEIVER)
if not STATUS:
    sys.exit(RECEIVER_ACC)

SENDER_ACC_SEQ, RECEIVER_ACC_SEQ = int(SENDER_ACC["sequence"]), int(
    RECEIVER_ACC["sequence"]
)

# Generating unsigned transactions with a single transfer message
STATUS, UNSIGNED_TX_TO = create_unsigned_txs(
    SENDER, RECEIVER, AMOUNT, "unsignedto.json"
)
if not STATUS:
    logging.error(UNSIGNED_TX_TO)

STATUS, UNSIGNED_TX_FROM = create_unsigned_txs(
    RECEIVER, SENDER, AMOUNT, "unsignedfrom.json"
)
if not STATUS:
    logging.error(UNSIGNED_TX_FROM)

for i in range(NUM_TXS):

    # Duplicating and appending transfer message in the existing array
    # to create a multi-msg transaction.
    create_multi_messages(NUM_MSGS, "unsignedto.json")
    create_multi_messages(NUM_MSGS, "unsignedfrom.json")

    # Signing and broadcasting the unsigned transactions from sender to receiver
    seqto = SENDER_ACC_SEQ + i
    status, txHash = sign_and_broadcast_txs(
        "unsignedto.json", "signedto.json", SENDER, seqto
    )
    if not status:
        logging.error(
            "sign_and_broadcast_tx from sender to receiver failed : %s", txHash
        )
    else:
        logging.info("broadcasted txhash: %s", txHash)

    # Signing and broadcasting the unsigned transactions from receiver to sender
    seqfrom = RECEIVER_ACC_SEQ + i
    status, txHash = sign_and_broadcast_txs(
        "unsignedfrom.json", "signedfrom.json", RECEIVER, seqfrom
    )
    if not status:  # if the txn is unsuccessful
        logging.error(
            "sign_and_broadcast_tx from receiver to sender failed : %s", txHash
        )
    else:
        logging.info("broadcasted txhash: %s", txHash)

logging.info("waiting for tx confirmation, avg time is 7s.")
time.sleep(7)

# Verifying the balance deductions
STATUS, SENDER_BAL_AFTER = query_balances(SENDER)
if not status:
    sys.exit(SENDER_BAL_AFTER)
SENDER_BAL_AFTER = SENDER_BAL_AFTER["balances"][0]["amount"]

STATUS, RECEIVER_BAL_AFTER = query_balances(RECEIVER)
if not status:
    sys.exit(RECEIVER_BAL_AFTER)
RECEIVER_BAL_AFTER = RECEIVER_BAL_AFTER["balances"][0]["amount"]

SENDER_DIFF = int(SENDER_BAL_AFTER) - int(SENDER_BAL_AFTER)
RECEIVER_DIFF = int(RECEIVER_BAL_BEFORE) - int(RECEIVER_BAL_AFTER)

print_balance_deductions("sender", SENDER_DIFF)
print_balance_deductions("receiver", RECEIVER_DIFF)
