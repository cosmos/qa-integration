"""
This script test a series of bank transfer transactions with single message between two accounts.
It takes two optional arguments namely -s(sender) and -r(receiver).
"""
import sys
from internal.core.parser import Parser
from internal.stats.stats import clear_data_by_type, print_stats
from internal.modules.auth.query import get_sequences
from internal.modules.bank.query import calculate_balance_deductions, query_balances
from internal.modules.bank.tx import tx_send

p = Parser(
    "This program takes inputs for intializing single message load test.",
    True,
    True,
    True,
)
sender, receiver, num_txs = p.get_args()
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
sender_acc_seq, receiver_acc_seq = get_sequences(sender, receiver)

# clearing db data with same test type
clear_data_by_type()

for i in range(num_txs):
    seqto = sender_acc_seq + i
    seqfrom = receiver_acc_seq + i
    status, sTxto = tx_send(sender, receiver, amount_to_be_sent, 100000, False, seqto)
    status, sTxfrom = tx_send(
        receiver, sender, amount_to_be_sent, 100000, False, seqfrom
    )

#### Print Balances ####
calculate_balance_deductions(sender, receiver, sender_balance_old, receiver_balance_old)

print_stats()
