import sys, time, logging
import unittest
from core.keys import keys_show
from modules.feegrant.tx import *
from modules.feegrant.query import *

from modules.bank.tx import (
    tx_send,
)
from modules.bank.query import (
    query_balances,
)

# get account addresses
granter = keys_show("account1")[1]["address"]
grantee = keys_show("account2")[1]["address"]
receiver = keys_show("validator1")[1]["address"]

amount = 5
fees = 2


class TestFeegrantModuleTxsQueries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # grant tx
        status, response = tx_grant("account1", grantee)
        assert status
        time.sleep(3)

        # set periodic grant by passing granter key and grantee address
        status, response = set_periodic_grant("account1", grantee)
        assert status
        time.sleep(3)

    def test_grant_tx(self):

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
        status, response = tx_send(grantee, receiver, amount, extra_args)
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

        self.assertEqual((granter_bal_old - fees), granter_bal_updated)
        self.assertEqual((grantee_bal_old - amount), grantee_bal_updated)
        self.assertEqual((receiver_bal_old + amount), receiver_bal_updated)

    def test_periodic_grant(self):

        # query grants to check if the periodic time is set or not
        status, periodic_grant = query_feegrant_grant(granter, grantee)
        self.assertTrue(status)
        spend_limit_before = int(
            periodic_grant["allowance"]["spend_limit"][0]["amount"]
        )

        # send tx
        extra_args = f"--fee-account {granter} --fees {fees}stake"
        status, response = tx_send(grantee, receiver, amount, extra_args)
        self.assertTrue(status)
        time.sleep(3)

        # query grants to check if the spend limti has changed or not.
        status, periodic_grant = query_feegrant_grant(granter, grantee)
        self.assertTrue(status)

        spend_limit_after = int(periodic_grant["allowance"]["spend_limit"][0]["amount"])
        self.assertEqual((spend_limit_before - fees), spend_limit_after)

    def test_query_feegrants(self):

        # test grants of grantee
        status, grantee_grants = query_greantee_grants(grantee)
        self.assertTrue(status)
        count = int(grantee_grants["pagination"]["total"])
        self.assertNotEqual(count, 0)
        granter_addr = grantee_grants["allowances"][0]["granter"]
        self.assertEqual(granter_addr, granter)

    def test_revoke_feegrant_tx(self):
        # revoke tx
        status, response = tx_revoke_feegrant("account1", grantee)
        self.assertTrue(status)
        time.sleep(3)

        status, grantee_grants = query_greantee_grants(grantee)
        self.assertTrue(status)
        count = int(grantee_grants["pagination"]["total"])
        self.assertEqual(count, 0)


if __name__ == "__main__":
    logging.info("INFO: running feegrant module tests")
    unittest.main()
