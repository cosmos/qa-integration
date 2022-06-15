import argparse, sys, logging
from core.keys import keys_show
from modules.auth.query import account_type, query_account
from modules.bank.tx import tx_send
from utils import validate_num_txs
from stats import clear_data_by_type, print_stats

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
    help="Receiver account number.",
)
parser.add_argument(
    "-n",
    "--num_txs",
    type=validate_num_txs,
    default=10000,
    help="Number of transactions to be made, should be positive integer",
)
args = parser.parse_args()

sender, receiver, num_txs = args.sender, args.receiver, int(args.num_txs)

# query account sequence
status, account = query_account(sender)
if not status:
    sys.exit(account)
seq1no = int(account["sequence"])
bound = num_txs + seq1no
logging.info(f"initial sequence number of sender account : {seq1no}")

# clearing db data with same test type
clear_data_by_type()

for i in range(seq1no, bound):
    status, tx = tx_send(sender, receiver, 1000000, 200000, sequence=i)

print_stats()
