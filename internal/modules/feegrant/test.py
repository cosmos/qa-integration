import sys, time, logging
import unittest
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

# logging.basicConfig(format="%(message)s", level=logging.DEBUG)

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


class TestFeegrantModuleTxsQueries(unittest.TestCase):
    def test_grant_tx(self):
        # grant tx
        status, response = tx_grant("account1", grantee)
        self.assertTrue(status)
        time.sleep(3)

        # query old balances of granter, grantee and reciver
        status, granter_bal_old = query_balances(granter)
        self.assertTrue(status)
        granter_bal_old = int(granter_bal_old["balances"][0]["amount"])

        status, grantee_bal_old = query_balances(grantee)
        self.assertTrue(status)
        grantee_bal_old = int(grantee_bal_old["balances"][0]["amount"])

        status, receiver_bal_old = query_balances(receiver)
        self.assertTrue(status)
        receiver_bal_old = int(receiver_bal_old["balances"][0]["amount"])

        # send tx
        extra_args = f"--fee-account {granter} --fees {fees}stake"
        status, response = tx_send(grantee, receiver, amount_to_sent, extra_args)
        self.assertTrue(status)
        time.sleep(3)

        # query new balances of granter, grantee and reciver
        status, granter_bal_updated = query_balances(granter)
        self.assertTrue(status)
        granter_bal_updated = int(granter_bal_updated["balances"][0]["amount"])

        status, grantee_bal_updated = query_balances(grantee)
        self.assertTrue(status)
        grantee_bal_updated = int(grantee_bal_updated["balances"][0]["amount"])

        status, receiver_bal_updated = query_balances(receiver)
        self.assertTrue(status)
        receiver_bal_updated = int(receiver_bal_updated["balances"][0]["amount"])

        assert (
            ((granter_bal_old - fees) == granter_bal_updated)
            & ((grantee_bal_old - amount_to_sent) == grantee_bal_updated)
            & (receiver_bal_old + amount_to_sent == receiver_bal_updated)
        ), f"error in grant tx!!!"

        # revoke tx
        status, response = tx_revoke_feegrant("account1", grantee)
        self.assertTrue(status)
        time.sleep(3)

    def test_periodic_grant(self):
        # set periodic grant by passing granter key and grantee address
        status, response = set_periodic_expiration_grant("account1", grantee)
        self.assertTrue(status)
        time.sleep(3)

        # query grants to check if the periodic time is set or not
        status, periodic_grant = query_feegrant_grant(granter, grantee)
        self.assertTrue(status)
        spend_limit_before = int(
            periodic_grant["allowance"]["basic"]["spend_limit"][0]["amount"]
        )

        # send tx
        extra_args = f"--fee-account {granter} --fees {fees}stake"
        status, response = tx_send(grantee, receiver, amount_to_sent, extra_args)
        self.assertTrue(status)
        time.sleep(3)

        # query grants to check if the spend limti has changed or not.
        status, periodic_grant = query_feegrant_grant(granter, grantee)
        self.assertTrue(status)

        spend_limit_after = int(
            periodic_grant["allowance"]["basic"]["spend_limit"][0]["amount"]
        )
        assert (
            spend_limit_before - fees
        ) == spend_limit_after, f"period grant tx was failed!!!"

        # revoke tx
        status, response = tx_revoke_feegrant("account1", grantee)
        self.assertTrue(status)

        time.sleep(3)


if __name__ == "__main__":
    logging.info("INFO: running feegrant module tests")
    unittest.main()
    logging.info("PASS: all feegrant module tests")
