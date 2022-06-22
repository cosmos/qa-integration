"""
This script floods the network with balance queries, delegation queries and staking queries.
It creates a load of 10,000 querires.
"""
import argparse
import sys
import logging
from core.keys import keys_show
from modules.auth.query import account_type
from modules.bank.query import query_balances
from modules.staking.query import query_staking_delegations, query_staking_validators
from utils import validate_num_txs
from stats import print_stats, clear_data_by_type, QUERY_TYPE

<<<<<<< HEAD:internal/load_test/query_load.py

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

=======
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

>>>>>>> 8cabbdd26e88f5b787bc9210a25464f1ef91e19b:internal/load-test/query_load.py
parser = argparse.ArgumentParser(
    description="This program takes inputs for intializing tx query load test."
)
parser.add_argument(
    "-s",
    "--sender",
    type=account_type,
    default=keys_show("validator1")[1]["address"],
    help="From which account the transaction should be intialized",
)
parser.add_argument(
    "-n",
    "--num_txs",
    type=validate_num_txs,
    default=1000,
    help="Number of transactions to be made, should be positive integer",
)
args = parser.parse_args()

sender, num_txs = args.sender, int(args.num_txs)

status, val1 = keys_show(sender, "val")
if not status:
    sys.exit(val1)
val1 = val1["address"]
<<<<<<< HEAD:internal/load_test/query_load.py
=======


# clearing db data with same test type
clear_data_by_type()
>>>>>>> 8cabbdd26e88f5b787bc9210a25464f1ef91e19b:internal/load-test/query_load.py

for i in range(0, num_txs):
    # Fetch balance of sender
    status, balance_query_response = query_balances(sender)
    if not status:
        logging.error(balance_query_response)
    else:
        balance = balance_query_response["balances"][0]
        logging.info("Balance :: %s", balance)

    # Fetch staking validators
    status, validators_response = query_staking_validators()
    if not status:
        logging.error(validators_response)

    # Fetch staking delegations
    status, delegations_response = query_staking_delegations(sender, val1)
    if not status:
        logging.error(delegations_response)

print_stats(QUERY_TYPE)
