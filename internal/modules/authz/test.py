import os
import sys, time, logging
import tempfile
from core.keys import keys_show
from modules.bank.query import (
    query_balances,
)
from modules.authz.tx import (
    tx_grant_authz,
    create_unsigned_send_tx,
    execute_authz_tx,
    tx_revoke_authz,
)
from modules.authz.query import (
    query_authz_grants,
)

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

# get account addresses
granter = keys_show("account1")[1]["address"]
grantee = keys_show("account2")[1]["address"]
receiver = keys_show("validator1")[1]["address"]
amount_to_be_sent = 5

temp = tempfile.TemporaryFile()
temp_file = f"{temp.name}.json"

if granter == grantee:
    sys.exit(
        'Error: The values of arguments "granter" and "grantee" are equal make sure to set different values'
    )


def authz_grant():
    # grant tx
    status, grant = tx_grant_authz(granter, grantee)
    assert status, f"error in grant tx :: {grant}"
    time.sleep(3)

    status, grants = query_authz_grants(granter, grantee)
    assert status, f"error while getting authz grants of {granter} and {grantee}!!!"

    spend_limit = grants["grants"][0]["authorization"]["spend_limit"][0]["amount"]
    if spend_limit != "":
        print(f"successfully grant authorization to {grantee}!!!")


def exec_tx():
    # query old balances of granter and reciver
    status, granter_bal_old = query_balances(granter)
    assert status, f"error while getting granter bal :: {status}"
    granter_bal_old = int(granter_bal_old["balances"][0]["amount"])

    status, receiver_bal_old = query_balances(receiver)
    assert status, f"error while getting grantee bal :: {status}"
    receiver_bal_old = int(receiver_bal_old["balances"][0]["amount"])

    # Generating unsigned transactions with a single transfer message
    status, unsignedTxto = create_unsigned_send_tx(
        granter, receiver, amount_to_be_sent, temp_file
    )
    assert status, f"error while creating unsigned send tx :: {unsignedTxto}"

    # executing generated authz transfer tx from grantee
    status, tx = execute_authz_tx("account2", temp_file)
    assert status, f"error while executing auth ecec tx :: {tx}"
    time.sleep(3)

    # query new balances of granter and reciver
    status, granter_bal_updated = query_balances(granter)
    assert status, f"error while getting granter bal :: {status}"
    granter_bal_updated = int(granter_bal_updated["balances"][0]["amount"])

    status, receiver_bal_updated = query_balances(receiver)
    assert status, f"error while getting grantee bal :: {status}"
    receiver_bal_updated = int(receiver_bal_updated["balances"][0]["amount"])

    if ((granter_bal_old - amount_to_be_sent) == granter_bal_updated) & (
        receiver_bal_old + amount_to_be_sent == receiver_bal_updated
    ):
        print(f"successfully executed tx on behalf of granter!!!")
    else:
        print(f"error while executing tx on behalf of granter!!!")


def revoke_tx():
    # revoke authz grants
    status, tx = tx_revoke_authz(granter, grantee)
    assert status, f"error while revoking grants :: {tx}"
    time.sleep(3)

    status, grants = query_authz_grants(granter, grantee)
    assert status, f"error while getting authz grants of {granter} and {grantee}!!!"

    a = grants["pagination"]["total"]
    assert len(grants), f"authz revoke tx failed!!!"

    # close and remove temp file
    temp.close()
    os.remove(temp_file)


# calls tests
authz_grant()
exec_tx()
revoke_tx()
