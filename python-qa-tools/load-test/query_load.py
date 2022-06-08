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
from utils import num_txs_type


logging.basicConfig(format='%(message)s',
                    level=logging.DEBUG)

PARSER = argparse.ArgumentParser(
    description='This program takes inputs for intializing tx query load test.'
)
PARSER.add_argument('-s', '--sender',
                    type=account_type,
                    default=keys_show("validator1")[1]['address'],
                    help='From which account the transaction should be intialized')
PARSER.add_argument('-n', '--num_txs',
                    type=num_txs_type,
                    default=1000,
                    help='Number of transactions to be made, atleast should be 1000')
ARGS = PARSER.parse_args()

SENDER, NUM_TXS = ARGS.sender, int(ARGS.num_txs)

STATUS, VAL1 = keys_show(SENDER, "val")
if not STATUS:
    sys.exit(VAL1)
VAL1 = VAL1['address']

for i in range(0, NUM_TXS):
    # Fetch balance of sender
    status, balance_query_response = query_balances(SENDER)
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
    status, delegations_response = query_staking_delegations(SENDER, VAL1)
    if not status:
        logging.error(delegations_response)
