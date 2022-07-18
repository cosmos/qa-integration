"""
This script test a series of bank transfer transactions with single message between two accounts.
It takes two optional arguments namely -s(sender) and -r(receiver).
"""
import sys, time
import utils
from internal.core.parser import ParseTestsDefaultFlags
from internal.stats.stats import clear_data_by_type, print_stats
from internal.modules.auth.query import query_account
from internal.modules.bank.query import calculate_balance_deductions, query_balances
from internal.modules.bank.tx import tx_send

num_txs = utils.env.NUM_TXS

p = ParseTestsDefaultFlags(
    desc="This program takes inputs for intializing single message load test.",
    sender=True,
    receiver=True,
)
sender, receiver = p.get_args()
amount_to_be_sent = 1000000

# Fetch Balances from sender receiver
status, sender_balance_old = query_balances(sender)
if not status:
    sys.exit(sender_balance_old)
sender_balance_old = sender_balance_old["balances"][0]["amount"]

status, receiver_balance_old = query_balances(receiver)
if not status:
    sys.exit(receiver_balance_old)
receiver_balance_old = receiver_balance_old["balances"][0]["amount"]

#### Fetching sequence numbers of to and from accounts
status, sender_acc = query_account(sender)
if not status:
    sys.exit(sender_acc)
sender_acc_seq = int(sender_acc["sequence"])

status, receiver_acc = query_account(receiver)
if not status:
    sys.exit(receiver_acc)
receiver_acc_seq = int(receiver_acc["sequence"])

# clearing db data with same test type
clear_data_by_type()

for i in range(num_txs):
    seqto = sender_acc_seq + i
    seqfrom = receiver_acc_seq + i
    status, sTxto = tx_send(sender, receiver, amount_to_be_sent, 100000, False, seqto)
    status, sTxfrom = tx_send(
        receiver, sender, amount_to_be_sent, 100000, False, seqfrom
    )

time.sleep(1)

#### Print Balances ####
calculate_balance_deductions(sender, receiver, sender_balance_old, receiver_balance_old)

print_stats()
