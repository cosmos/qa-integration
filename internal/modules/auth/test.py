"""
This module contains all auth test functions.
"""
import unittest
import os
import json

from core.keys import keys_add, keys_show
from modules.auth.query import (
    query_account,
    query_accounts,
    query_params,
)
from internal.core.tx import tx_sign
from internal.modules.auth.tx import tx_decode, tx_encode
from internal.modules.bank.tx import create_unsigned_txs


HOME = os.getenv("HOME")
DEFAULT_GAS = 2000000


class TestAuthModuleTxsQueries(unittest.TestCase):
    """
    The class `TestAuthModuleTxsQueries` contains test functions
    which test queries of auth module
    """

    @classmethod
    def setUpClass(cls):
        """
        The function `setUpClass` will be called before running any test case.
        """
        status, _ = keys_add("multisigaccount", True)
        assert status, "Failed to add multisig account"

        status, _ = keys_show("multisigaccount")
        assert status, "Failed to show multisig account"

    def test_query_account(self):
        """
        The function `test_query_account` will query account
        and test balance
        """
        status, key = keys_show("account1", "acc")
        self.assertTrue(status, key)
        self.assertTrue(key)
        status, query_response = query_account(key["address"])
        self.assertTrue(status, query_response)

    def test_query_account_fail(self):
        """
        The function `test_query_account_fail` will query wrong account
        and assert fail condition
        """
        status, response = query_account(
            "cosmos1xpcfd7pxfmv6gd50y9mwjq50kwqpqrh5mmw72h"
        )
        self.assertFalse(status, response)

    def test_query_accounts(self):
        """
        The function `test_query_accounts` will query accounts
        and test balance
        """
        status, query_response = query_accounts()
        self.assertTrue(status, query_response)

    def test_query_params(self):
        """
        The function `test_query_params` will query params
        and test gas
        """
        status, query_resp = query_params()
        self.assertTrue(status, query_resp)

    def test_tx_encode_and_decode(self):
        """
        The function `test_tx_encode_and_decode` will encode and decode a transaction.
        """
        status, from_account = keys_show("account1", "acc")
        self.assertTrue(status, from_account)

        from_address = from_account["address"]
        status, account_resp = query_account(from_address)

        self.assertTrue(status, account_resp)
        from_address_sequence = account_resp["sequence"]

        status, to_account = keys_show("account2", "acc")
        self.assertTrue(status, to_account)
        to_address = to_account["address"]

        status, unsigned_tx = create_unsigned_txs(
            from_address, to_address, "100stake", "unsigned_tx.json"
        )
        self.assertTrue(status, unsigned_tx)

        status, signed_tx = tx_sign(
            "unsigned_tx.json", from_address, from_address_sequence, DEFAULT_GAS
        )
        self.assertTrue(status, signed_tx)
        with open(HOME + "/" + "signed_tx.json", "w", encoding="utf8") as outfile:
            json.dump(signed_tx, outfile)

        status, encoded_tx = tx_encode("signed_tx.json")
        self.assertTrue(status, encoded_tx)

        status, decoded_json = tx_decode(encoded_tx)
        self.assertTrue(status, decoded_json)
        self.assertEqual(str(signed_tx), str(decoded_json))


if __name__ == "__main__":
    unittest.main()
