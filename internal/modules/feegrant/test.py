import sys, time, logging
from core.keys import keys_show
from modules.feegrant.tx import (
    tx_grant,
    tx_revoke_feegrant,
    set_periodic_expiration_grant,
)
from modules.feegrant.query import (
    query_feegrant_grant,
)

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

# get account addresses
address_1 = keys_show("account1")[1]["address"]
address_2 = keys_show("account2")[1]["address"]

if address_1 == address_2:
    sys.exit(
        'Error: The values of arguments "granter" and "grantee" are equal make sure to set different values'
    )


def grant_tx():
    # grant tx
    status, grant = tx_grant("account1", address_2)
    if not status:
        logging.error(f"error in grant tx :: {grant}")
    else:
        logging.info(f"tx_hash of grant_tx :: {grant['txhash']}")

    time.sleep(3)

    # query free grant of granter and grantee
    status, grant = query_feegrant_grant(address_1, address_2)
    if not status:
        logging.error(f"grant tx failed :: {status}")
    else:
        if ( grant["granter"] == address_1 ) & (grant["grantee"] == address_2):
            logging.info(f"grant tx is successfull!!!")

    # revoke tx
    status, revoke = tx_revoke_feegrant("account1", address_2)
    if not status:
        logging.error(f"error in revoke fee grant tx :: {revoke}")
    else:
        logging.info(f"tx_hash of revoke fee grant :: {revoke['txhash']}")

    time.sleep(3)


def periodic_grant():
    # periodic grant
    status, gr = set_periodic_expiration_grant("account1", address_2)
    if not status:
        logging.error(f"error in periodic grant tx :: {gr}")
    else:
        logging.info(f"tx_hash of periodic grant_tx :: {gr['txhash']}")

    time.sleep(3)

    # query periodic grants
    status, periodic_grant = query_feegrant_grant(address_1, address_2)
    if not status:
        logging.error(f"periodic grant tx failed :: {status}")
    else:
        if periodic_grant["allowance"]["period"] is not None:
            logging.info(f"periodic grant tx is successfull!!!")

     # revoke tx
    status, revoke = tx_revoke_feegrant("account1", address_2)
    if not status:
        logging.error(f"error in revoke fee grant tx :: {revoke}")
    else:
        logging.info(f"tx_hash of revoke fee grant :: {revoke['txhash']}")

    time.sleep(3)


grant_tx()
periodic_grant()
