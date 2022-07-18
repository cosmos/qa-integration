"""
This script creates a load of 10,000 `send` transactions and floods the network.
"""
import sys
import logging
import utils
from internal.core.parser import ParseTestsDefaultFlags
from internal.stats.stats import clear_data_by_type, print_stats
from internal.modules.auth.query import query_account
from internal.modules.bank.tx import tx_send

num_txs = utils.env.NUM_TXS

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

p = ParseTestsDefaultFlags(
    desc="This program takes inputs for intializing send load test.",
    sender=True,
    receiver=True,
)
sender, receiver = p.get_args()
amount_to_be_sent = 1000000

# query account sequence
status, account = query_account(sender)
if not status:
    sys.exit(account)
seq1no = int(account["sequence"])
bound = num_txs + seq1no
logging.info("initial sequence number of sender account : %s", seq1no)

# clearing db data with same test type
clear_data_by_type()

for i in range(seq1no, bound):
    status, tx = tx_send(sender, receiver, amount_to_be_sent, 200000, sequence=i)

print_stats()
