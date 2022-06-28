import sys, time, logging
from core.keys import keys_show
from modules.feegrant.tx import (
    tx_grant,
    tx_revoke_feegrant,
)
from modules.feegrant.query import (
    query_feegrant_grant,
)

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

# get validator, delegator and dst validator address
granter = keys_show("account1")[1]["address"]
grantee = keys_show("account2")[1]["address"]

if granter == grantee:
    sys.exit(
        'Error: The values of arguments "granter" and "grantee" are equal make sure to set different values'
    )

# grant tx
status, grant = tx_grant("account1", grantee)
if not status:
    logging.error(f"error in grant tx :: {grant}")
else:
    logging.info(f"tx_hash of grant_tx :: {grant['txhash']}")

time.sleep(3)

# query free grant of granter and grantee
status, grant = query_feegrant_grant(granter, grantee)
if not status:
    logging.error(f"grant tx failed :: {status}")
else:
    if ( grant["granter"] == granter ) & (grant["grantee"] == grantee):
        logging.info(f"grant tx is successfull!!!")

# revoke tx
status, revoke = tx_revoke_feegrant("account1", grantee)
if not status:
    logging.error(f"error in revoke fee grant tx :: {revoke}")
else:
    logging.info(f"tx_hash of revoke fee grant :: {revoke['txhash']}")

time.sleep(3)
