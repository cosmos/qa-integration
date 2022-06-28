"""
This script test a series of bank transfer transactions with multiple messages between two accounts.
It takes two optional arguments namely -s(sender) and -r(receiver)
"""
import os
import sys
import logging
from internal.core.parser import Parser
from internal.stats.stats import clear_data_by_type, print_stats
from internal.modules.auth.query import get_sequences
from internal.modules.bank.query import calculate_balance_deductions, query_balances
from internal.modules.bank.tx import sign_and_broadcast_txs, create_unsigned_txs
from internal.utils import create_multi_messages

HOME = os.getenv("HOME")
NUM_MSGS = int(os.getenv("NUM_MSGS"))

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

p = Parser(
    "This program takes inputs for intializing multi messages load test.",
    True,
    True,
    True,
)
args = p.parser.parse_args()
sender, receiver, num_txs = args.sender, args.receiver, int(args.num_txs)
amount_to_be_sent = 1000000

if sender == receiver:
    sys.exit(
        """Error: The values of arguments "sender" \
                and "receiver" are equal make sure to set \
                    different values"""
    )
# Fetch balances of sender and receiver accounts before executing the load test
status, sender_balance_old = query_balances(sender)
if not status:
    sys.exit(sender_balance_old)
sender_balance_old = int(sender_balance_old["balances"][0]["amount"])

# Fetch Balances of receiver executing the load test
status, receiver_balance_old = query_balances(receiver)
if not status:
    sys.exit(receiver_balance_old)
receiver_balance_old = int(receiver_balance_old["balances"][0]["amount"])

# Fetching sequence numbers of to and from accounts
sender_acc_seq, receiver_acc_seq = get_sequences(sender, receiver)

# Generating unsigned transactions with a single transfer message
status, unsignedTxto = create_unsigned_txs(
    sender, receiver, amount_to_be_sent, "unsignedto.json"
)
if not status:
    logging.error(unsignedTxto)

status, unsignedTxfrom = create_unsigned_txs(
    receiver, sender, amount_to_be_sent, "unsignedfrom.json"
)
if not status:
    logging.error(unsignedTxfrom)


# clearing db data with same test type
clear_data_by_type()

for i in range(num_txs):

    # Duplicating and appending transfer message
    # in the existing array to create a multi-msg transaction
    create_multi_messages(NUM_MSGS, "unsignedto.json")
    create_multi_messages(NUM_MSGS, "unsignedfrom.json")

    # Signing and broadcasting the unsigned transactions from sender to receiver
    seqto = sender_acc_seq + i
    logging.info("Signing and broadcasting tx: %s", i * 2 + 1)
    status, tx = sign_and_broadcast_txs(
        "unsignedto.json", "signedto.json", sender, seqto
    )

    # Signing and broadcasting the unsigned transactions from receiver to sender
    seqfrom = receiver_acc_seq + i
    logging.info("Signing and broadcasting tx: %s", i * 2 + 2)
    status, tx = sign_and_broadcast_txs(
        "unsignedfrom.json", "signedfrom.json", receiver, seqfrom
    )

# Verifying the Balances
calculate_balance_deductions(sender, receiver, sender_balance_old, receiver_balance_old)

print_stats()
