import os
import time, logging
import tempfile
import unittest
from core.keys import keys_show
from modules.bank.query import (
    query_balances,
)
from modules.authz.tx import *
from modules.authz.query import *

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

# get account addresses
granter = keys_show("account1")[1]["address"]
grantee = keys_show("account2")[1]["address"]
receiver = keys_show("validator1")[1]["address"]
amount = 5

temp = tempfile.TemporaryFile()
temp_file = f"{temp.name}.json"


class TestAuthzModuleTxsQueries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # grant tx
        status, grant = tx_grant_authz(granter, grantee)
        assert status, "error in authz grant tx!!!"
        time.sleep(3)

    def test_authz_grant(self):
        status, grants = query_authz_grants(granter, grantee)
        self.assertTrue(status)
        spend_limit = grants["grants"][0]["authorization"]["spend_limit"][0]["amount"]
        self.assertIsNotNone(spend_limit)

    def test_query_authz_grants(self):
        # test grants granted to a grantee
        status, grantee_grants = query_authz_grantee_grants(grantee)
        self.assertTrue(status)
        count = int(grantee_grants["pagination"]["total"])
        self.assertNotEqual(count, 0)
        granter_addr = grantee_grants["grants"][0]["granter"]
        self.assertEqual(granter_addr, granter)

        # test grants granted granted by a granter
        status, granter_grants = query_authz_granter_grants(granter)
        self.assertTrue(status)
        count = int(granter_grants["pagination"]["total"])
        self.assertNotEqual(count, 0)
        grantee_addr = granter_grants["grants"][0]["grantee"]
        self.assertEqual(grantee_addr, grantee)

    def test_exec_tx(self):
        # query old balances of granter and reciver
        status, granter_bal_old = query_balances(granter)
        self.assertTrue(status)
        granter_bal_old = int(granter_bal_old["balances"][0]["amount"])

        status, receiver_bal_old = query_balances(receiver)
        self.assertTrue(status)
        receiver_bal_old = int(receiver_bal_old["balances"][0]["amount"])

        # Generating unsigned transactions with a single transfer message
        status, unsignedTxto = create_unsigned_send_tx(
            granter, receiver, amount, temp_file
        )
        self.assertTrue(status)
        time.sleep(3)

        # executing generated authz transfer tx from grantee
        status, tx = execute_authz_tx("account2", temp_file)
        self.assertTrue(status)
        time.sleep(3)

        # query new balances of granter and reciver
        status, granter_bal_updated = query_balances(granter)
        self.assertTrue(status)
        granter_bal_updated = int(granter_bal_updated["balances"][0]["amount"])

        status, receiver_bal_updated = query_balances(receiver)
        self.assertTrue(status)
        receiver_bal_updated = int(receiver_bal_updated["balances"][0]["amount"])
        self.assertEqual((granter_bal_old - amount), granter_bal_updated)
        self.assertEqual((receiver_bal_old + amount), receiver_bal_updated)

    def test_revoke_tx(self):
        # revoke authz grants
        status, tx_res = tx_revoke_authz(granter, grantee)
        self.assertTrue(status)
        time.sleep(3)

        status, grants = query_authz_grants(granter, grantee)
        self.assertTrue(status)
        count = int(grants["pagination"]["total"])
        self.assertEqual(count, 0)

        # close and remove temp file
        temp.close()
        os.remove(temp_file)


if __name__ == "__main__":
    logging.info("INFO: running authz module tests")
    unittest.main()
