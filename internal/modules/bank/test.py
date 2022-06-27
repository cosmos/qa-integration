import time, logging
from core.keys import keys_show
from modules.bank.tx import (
    tx_send,
)
from modules.bank.query import (
    query_balances,
)

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

sender = keys_show("account1")[1]["address"]
receiver = keys_show("account2")[1]["address"]

# assign the arguments
amount_to_be_sent = 5

if sender == receiver:
    logging.error(f"Error: The values of arguments sender and receiver are equal make sure to set different values")

# Fetch balances of sender and receiver accounts before executing the send_tx
status, sender_balance_old = query_balances(sender)
if not status:
    logging.error(sender_balance_old)
sender_balance_old = int(sender_balance_old["balances"][0]["amount"])

# Fetch balances of receiver
status, receiver_balance_old = query_balances(receiver)
if not status:
    logging.error(receiver_balance_old)
receiver_balance_old = int(receiver_balance_old["balances"][0]["amount"])

# send tx
status, send_tx = tx_send(sender, receiver, amount_to_be_sent)
if not status:
    logging.error(f"send tx status:: {status}")
else:
    logging.info(f"tx_hash of send :: {send_tx['txhash']}")

time.sleep(3)

# Fetch new balances of sender and receiver accounts after executing send_tx
status, sender_balance_new = query_balances(sender)
if not status:
    logging.error(sender_balance_new)
sender_balance_new = int(sender_balance_new["balances"][0]["amount"])

# Fetch balances of receiver
status, receiver_balance_new = query_balances(receiver)
if not status:
    logging.error(receiver_balance_new)
receiver_balance_new = int(receiver_balance_new["balances"][0]["amount"])

if ((sender_balance_old - amount_to_be_sent) == sender_balance_new) & (
    (receiver_balance_old + amount_to_be_sent) == receiver_balance_new
):
    logging.info(f"send tx is successfull!!")
else:
    logging.error(f"send tx failed!!")
