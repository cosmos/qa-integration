"""
This script test a series of bank transfer transactions with multiple messages between two accounts.
It takes two optional arguments namely -s(sender) and -r(receiver)
"""
import argparse
import os
import sys
import time
import logging
from core.keys import keys_show
from modules.auth.query import account_type, query_account
from modules.bank.query import query_balances
from modules.bank.tx import sign_and_broadcast_txs, create_unsigned_txs
from utils import create_multi_messages, print_balance_deductions

HOME = os.getenv('HOME')
NUM_MSGS = int(os.getenv('NUM_MSGS'))
logging.basicConfig(format='%(message)s',
                    level=logging.DEBUG)

PARSER = argparse.ArgumentParser(
    description='This program takes inputs for intializing multi message load test.'
)
PARSER.add_argument(
    '-s', '--sender',
    type=account_type,
    default=keys_show("account1")[1]['address'],
    help='Sender bech32 address')
PARSER.add_argument(
    '-r', '--receiver',
    type=account_type,
    default=keys_show("account2")[1]['address'],
    help='Receiver bech32 address')
PARSER.add_argument(
    '-n', '--num_txs',
    type=int,
    default=1000,
    help='Number of transactions to be made, atleast should be 1000')
ARGS = PARSER.parse_args()
SENDER = ARGS.sender
RECEIVER = ARGS.receiver
NUM_TXS = int(ARGS.num_txs)
AMOUNT_TO_BE_SENT = 1000000

if SENDER == RECEIVER:
    sys.exit('''Error: The values of arguments "sender" and "receiver"
            are equal make sure to set different values''')

# Fetch balances of sender and receiver accounts before executing the load test
STATUS, SENDER_BALANCE_OLD = query_balances(SENDER)
if not STATUS:
    sys.exit(SENDER_BALANCE_OLD)
SENDER_BALANCE_OLD = int(SENDER_BALANCE_OLD['balances'][0]['amount'])

# Fetch Balances of receiver executing the load test
STATUS, RECEIVER_BALANCE_OLD = query_balances(RECEIVER)
if not STATUS:
    sys.exit(RECEIVER_BALANCE_OLD)
RECEIVER_BALANCE_OLD = int(RECEIVER_BALANCE_OLD['balances'][0]['amount'])

# Fetching sequence numbers of to and from accounts
STATUS, SENDER_ACC_SEQ = query_account(SENDER)
if not STATUS:
    sys.exit(SENDER_ACC_SEQ)

STATUS, RECEIVER_ACC_SEQ = query_account(RECEIVER)
if not STATUS:
    sys.exit(RECEIVER_ACC_SEQ)

SEQ1NO, SEQ2NO = int(SENDER_ACC_SEQ['sequence']), int(
    RECEIVER_ACC_SEQ['sequence'])

# Generating unsigned transactions with a single transfer message
STATUS, UNSIGNED_TX_TO = create_unsigned_txs(
    SENDER, RECEIVER, AMOUNT_TO_BE_SENT, 'unsignedto.json')
if not STATUS:
    logging.error(UNSIGNED_TX_TO)

STATUS, UNSIGNED_TX_FROM = create_unsigned_txs(
    RECEIVER,
    SENDER,
    AMOUNT_TO_BE_SENT,
    'unsignedfrom.json')
if not STATUS:
    logging.error(UNSIGNED_TX_FROM)

for i in range(NUM_TXS):

    # Duplicating and appending transfer message in the existing array
    # to create a multi-msg transaction.
    create_multi_messages(NUM_MSGS, 'unsignedto.json')
    create_multi_messages(NUM_MSGS, 'unsignedfrom.json')

    # Signing and broadcasting the unsigned transactions from sender to receiver
    seqto = SEQ1NO + i
    status, txHash = sign_and_broadcast_txs(
        'unsignedto.json', 'signedto.json', SENDER, seqto)
    if not status:
        logging.error(
            "sign_and_broadcast_tx from sender to receiver failed : %s", txHash)
    else:
        logging.info("broadcasted txhash: %s", txHash)

    # Signing and broadcasting the unsigned transactions from receiver to sender
    seqfrom = SEQ1NO + i
    status, txHash = sign_and_broadcast_txs(
        'unsignedfrom.json',
        'signedfrom.json',
        RECEIVER,
        seqfrom)
    if not status:  # if the txn is unsuccessful
        logging.error(
            "sign_and_broadcast_tx from receiver to sender failed : %s", txHash)
    else:
        logging.info("broadcasted txhash: %s", txHash)

logging.info('waiting for tx confirmation, avg time is 7s.')
time.sleep(7)

# Verifying the balance deductions
STATUS, SENDER_BALANCE_UPDATED = query_balances(SENDER)
if not status:
    sys.exit(SENDER_BALANCE_UPDATED)
SENDER_BALANCE_UPDATED = SENDER_BALANCE_UPDATED['balances'][0]['amount']

STATUS, RECEIVER_BALANCE_UPDATED = query_balances(RECEIVER)
if not status:
    sys.exit(RECEIVER_BALANCE_UPDATED)
RECEIVER_BALANCE_UPDATED = RECEIVER_BALANCE_UPDATED['balances'][0]['amount']

SENDER_DIFF = int(SENDER_BALANCE_OLD) - int(SENDER_BALANCE_UPDATED)
RECEIVER_DIFF = int(RECEIVER_BALANCE_OLD) - int(RECEIVER_BALANCE_UPDATED)

print_balance_deductions('sender', SENDER_DIFF)
print_balance_deductions('receiver', RECEIVER_DIFF)
