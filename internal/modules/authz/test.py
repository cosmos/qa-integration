from os import stat_result
import sys, time, logging
from core.keys import keys_show
from modules.bank.tx import (
    DEFAULT_GAS,
    tx_send,
)
from modules.bank.query import (
    query_balances,
)
from modules.authz.tx import (
    tx_grant_authz,
    create_unsigned_send_tx,
    execute_authz_tx,
)

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

# get account addresses
granter = keys_show("account1")[1]["address"]
grantee = keys_show("account2")[1]["address"]
receiver = keys_show("validator1")[1]["address"]
amount_to_be_sent = 5
fees = 2

print(f"granter......{granter}")
print(f"grantee........{grantee}")
print(f"receiver.......{receiver}")

if granter == grantee:
    sys.exit(
        'Error: The values of arguments "granter" and "grantee" are equal make sure to set different values'
    )

# grant tx
status, grant = tx_grant_authz(granter, grantee)
print(f"granttttttt..........{grant}")
assert status, f"error in grant tx :: {grant}"
time.sleep(3)

# Generating unsigned transactions with a single transfer message
status, unsignedTxto = create_unsigned_send_tx(
    granter, receiver, amount_to_be_sent, "send_tx.json"
)
assert status, f"error while creating unsigned send tx !!!"

status, tx = execute_authz_tx("account2","send_tx.json")
assert status, f"error while executing auth ecec tx :: {tx}"