"""
This script creates a load of 10,000 `send` transactions and floods the network.
"""
import argparse
import sys
import logging
from core.keys import keys_show
from modules.auth.query import account_type, query_account
from modules.bank.tx import tx_send

logging.basicConfig(format='%(message)s',
                    level=logging.DEBUG)

PARSER = argparse.ArgumentParser(
    description='This program takes inputs for intializing multi message load test.')
PARSER.add_argument('-s', '--sender',
                    type=account_type,
                    default=keys_show("account1")[1]['address'],
                    help='From which account the transaction should be intialized')
PARSER.add_argument('-r', '--receiver',
                    type=account_type,
                    default=keys_show("account2")[1]['address'],
                    help='Receiver account number.')
ARGS = PARSER.parse_args()

SENDER, RECEIVER = ARGS.sender, ARGS.receiver

# query account sequence
STATUS, SENDER_ACCOUNT = query_account(SENDER)
if not STATUS:
    sys.exit(SENDER_ACCOUNT)
SENDER_ACC_SEQ = int(SENDER_ACCOUNT['sequence'])
BOUND = 10000 + SENDER_ACC_SEQ
logging.info("initial sequence number of sender account : %s", SENDER_ACC_SEQ)

for i in range(SENDER_ACC_SEQ, BOUND):
    status, tx = tx_send(SENDER, RECEIVER, 1000000, 200000, sequence=i)
    if not status:
        logging.error(tx)
    else:
        TXHASH = tx['txhash']
        logging.info("TX HASH :: %s", TXHASH)
