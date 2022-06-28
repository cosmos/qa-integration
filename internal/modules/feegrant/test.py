import os, sys, time, logging
from core.keys import keys_show
from internal.utils import DAEMON, exec_command
import tempfile
from modules.feegrant.tx import (
    tx_grant,
)
from modules.feegrant.query import (
    query_feegrant_grants,
)

HOME = os.getenv("HOME")
DAEMON = os.getenv("DAEMON")
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

# get validator, delegator and dst validator address
granter = keys_show("account1")[1]["address"]
grantee = keys_show("account2")[1]["address"]

# assign the arguments
amount_to_be_sent = 5

if granter == grantee:
    sys.exit(
        'Error: The values of arguments "granter" and "grantee" are equal make sure to set different values'
    )

# delegate tx
status, grant = tx_grant("account1", grantee)
if not status:
    logging.error(f"error in grant tx :: {grant}")
else:
    logging.info(f"tx_hash of grant_tx :: {grant['txhash']}")

time.sleep(3)

status, grants = query_feegrant_grants(granter, grantee)
print(f"status and grants.............{status}{grants}")
