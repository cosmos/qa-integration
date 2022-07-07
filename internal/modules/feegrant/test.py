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
from modules.bank.tx import (
    DEFAULT_GAS,
    tx_send,
)
from modules.bank.query import (
    query_balances,
)

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

# get account addresses
granter = keys_show("account1")[1]["address"]
grantee = keys_show("account2")[1]["address"]
receiver = keys_show("validator1")[1]["address"]
amount_to_sent = 5
fees = 2

if granter == grantee:
    sys.exit(
        'Error: The values of arguments "granter" and "grantee" are equal make sure to set different values'
    )


def grant_tx():
    # grant tx
    status, grant = tx_grant("account1", grantee)
    assert status, f"error in grant tx :: {grant}"
    time.sleep(3)

    # query old balances of granter, grantee and reciver
    status, granter_bal_old = query_balances(granter)
    assert status, f"error while getting granter bal :: {status}"
    granter_bal_old = int(granter_bal_old["balances"][0]["amount"])

    status, grantee_bal_old = query_balances(grantee)
    assert status, f"error while getting grantee bal :: {status}"
    grantee_bal_old = int(grantee_bal_old["balances"][0]["amount"])

    status, receiver_bal_old = query_balances(receiver)
    assert status, f"error while getting receiver old bal :: {status}"
    receiver_bal_old = int(receiver_bal_old["balances"][0]["amount"])

    # send tx
    extra_args = f"--fee-account {granter} --fees {fees}stake"
    status, send = tx_send(grantee, receiver, amount_to_sent, extra_args)
    assert status, f"error inde send tx b/w grantee and granter : {send}"
    time.sleep(3)

    # query new balances of granter, grantee and reciver
    status, granter_bal_updated = query_balances(granter)
    assert status, f"error while getting granter bal :: {status}"
    granter_bal_updated = int(granter_bal_updated["balances"][0]["amount"])

    status, grantee_bal_updated = query_balances(grantee)
    assert status, f"error while getting grantee bal :: {status}"
    grantee_bal_updated = int(grantee_bal_updated["balances"][0]["amount"])

    status, receiver_bal_updated = query_balances(receiver)
    assert status, f"error while getting receiver bal :: {status}"
    receiver_bal_updated = int(receiver_bal_updated["balances"][0]["amount"])

    if (
        ((granter_bal_old - fees) == granter_bal_updated)
        & ((grantee_bal_old - amount_to_sent) == grantee_bal_updated)
        & (receiver_bal_old + amount_to_sent == receiver_bal_updated)
    ):
        print(f"grant tx is successfull!!!")
    else:
        print(f"error in grant tx!!!")

    # revoke tx
    status, revoke = tx_revoke_feegrant("account1", grantee)
    assert status, f"error in revoke fee grant tx :: {revoke}"

    time.sleep(3)


def periodic_grant():
    # set periodic grant by passing granter key and grantee address
    status, grant = set_periodic_expiration_grant("account1", grantee)
    assert status, f"tx_hash of periodic grant_tx :: {grant['txhash']}"
    time.sleep(3)

    # query grants to check if the periodic time is set or not
    status, periodic_grant = query_feegrant_grant(granter, grantee)
    if not status:
        logging.error(f"periodic grant tx failed :: {status}")
    else:
        if periodic_grant["allowance"]["period"] is not None:
            logging.info(f"set periodic grant tx!!!")
    spend_limit_before = int(
        periodic_grant["allowance"]["basic"]["spend_limit"][0]["amount"]
    )

    # send tx
    extra_args = f"--fee-account {granter} --fees {fees}stake"
    status, send = tx_send(grantee, receiver, amount_to_sent, extra_args)
    assert status, f"error inde send tx b/w grantee and granter : {send}"
    time.sleep(3)

    # query grants to check if the spend limti has changed or not.
    status, periodic_grant = query_feegrant_grant(granter, grantee)
    assert status, f"periodic grant tx failed :: {status}"

    spend_limit_after = int(
        periodic_grant["allowance"]["basic"]["spend_limit"][0]["amount"]
    )
    assert (
        spend_limit_before - fees
    ) == spend_limit_after, f"period grant tx was failed!!!"

    # revoke tx
    status, revoke = tx_revoke_feegrant("account1", grantee)
    assert status, f"error in revoke periodic feegrant tx :: {revoke}"

    time.sleep(3)


# call tests
grant_tx()
periodic_grant()
