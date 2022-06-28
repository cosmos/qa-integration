import argparse, sys, logging
import utils
from core.keys import keys_show
from modules.auth.query import account_type
from modules.bank.query import query_balances
from modules.staking.query import query_staking_delegations, query_staking_validators
from stats import print_stats, clear_data_by_type, QUERY_TYPE

num_txs = utils.env.NUM_TXS

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

parser = argparse.ArgumentParser(
    description="This program takes inputs for intializing query load test."
)
parser.add_argument(
    "-s",
    "--sender",
    type=account_type,
    default=keys_show("validator1")[1]["address"],
    help="From which account the transaction should be intialized",
)

args = parser.parse_args()

sender = args.sender

status, val1 = keys_show(sender, "val")
if not status:
    sys.exit(val1)
val1 = val1["address"]


# clearing db data with same test type
clear_data_by_type()

for i in range(0, num_txs):
    # Fetch balance of sender
    status, balance_query_response = query_balances(sender)
    if not status:
        logging.error(balance_query_response)
    else:
        balance = balance_query_response["balances"][0]
        logging.info(f"Balance :: {balance}")

    # Fetch staking validators
    status, validators_response = query_staking_validators()
    if not status:
        logging.error(validators_response)

    # Fetch staking delegations
    status, delegations_response = query_staking_delegations(sender, val1)
    if not status:
        logging.error(delegations_response)

print_stats(QUERY_TYPE)
