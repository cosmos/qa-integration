import os, sys, time, logging
from core.keys import keys_show
from internal.utils import DAEMON, exec_command
from modules.bank.tx import (
    tx_send,
)
from modules.bank.query import (
    query_balances,
)

HOME = os.getenv("HOME")
DAEMON = os.getenv("DAEMON")
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

# get validator, delegator and dst validator address
#validator = keys_show("validator1", "val", 1)[1]["address"]
from_address = keys_show("account1", "acc", 1)[1]["address"]
to_address = keys_show("account2", "acc", 1)[1]["address"]
#dst_val_address = keys_show("validator2", "val", 2)[1]["address"]

# assign the arguments
amount_to_be_sent = 5

if from_address == to_address:
    sys.exit(
        'Error: The values of arguments "sender" and "receiver" are equal make sure to set different values'
    )

# send tx
status, send_tx = tx_send(from_address, to_address, amount_to_be_sent)
if not status:
    logging.error(f"error in send tx :: {send_tx}")
else:
    logging.info(f"tx_hash of send :: {send_tx['txhash']}")

time.sleep(3)

print(f"send tx......{send_tx}")