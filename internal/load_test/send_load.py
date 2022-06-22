"""
This script creates a load of 10,000 `send` transactions and floods the network.
"""
import argparse
import sys
import logging
from core.keys import keys_show
from modules.auth.query import account_type, query_account
from modules.bank.tx import tx_send
from utils import validate_num_txs

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

parser = argparse.ArgumentParser(
    description="This program takes inputs for intializing multi message load test."
)
parser.add_argument(
    "-s",
    "--sender",
    type=account_type,
    default=keys_show("account1")[1]["address"],
    help="From which account the transaction should be intialized",
)
parser.add_argument(
    "-r",
    "--receiver",
    type=account_type,
    default=keys_show("account2")[1]["address"],
    help="receiver account number.",
)
parser.add_argument(
    "-n",
    "--num_txs",
    type=validate_num_txs,
    default=10000,
    help="Number of transactions to be made, should be positive integer",
)
args = parser.parse_args()

sender, receiver, num_txs = args.sender, args.receiver, args.num_txs

# query account sequence
status, sender_account = query_account(sender)
if not status:
    sys.exit(sender_account)
sender_acc_seq = int(sender_account["sequence"])
bound = num_txs + sender_acc_seq
logging.info("initial sequence number of sender account : %s", sender_acc_seq)

for i in range(sender_acc_seq, bound):
    status, tx = tx_send(sender, receiver, 1000000, 200000, sequence=i)
    if not status:
        logging.error(tx)
    else:
        tx_hash = tx["tx_hash"]
        logging.info("TX HASH :: %s", tx_hash)
