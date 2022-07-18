"""
This script floods the network with balance queries, delegation queries and staking queries.
It creates a load of 10,000 querires.
"""
import sys
import logging
import utils
from internal.core.parser import ParseTestsDefaultFlags
from internal.core.keys import keys_show
from internal.modules.bank.query import query_balances
from internal.modules.staking.query import (
    query_delegator_delegation,
    query_staking_validators,
)
from internal.stats.stats import print_stats, clear_data_by_type, QUERY_TYPE

num_txs = utils.env.NUM_TXS

logging.basicConfig(format="%(message)s", level=logging.DEBUG)
p = ParseTestsDefaultFlags(
    desc="Arguments to run the query_load test script",
    sender=True,
    sender_account="validator1",
    receiver=False,
)
sender, _ = p.get_args()
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
        logging.info("Balance :: %s", balance)
    # Fetch staking validators
    status, validators_response = query_staking_validators()
    if not status:
        logging.error(validators_response)

    # Fetch staking delegations
    status, delegations_response = query_delegator_delegation(sender, val1)
    if not status:
        logging.error(delegations_response)

print_stats(QUERY_TYPE)
