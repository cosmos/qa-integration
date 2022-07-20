"""
This module contains all auth test functions.
"""
import unittest
import os
import json

from core.keys import keys_show
from internal.core.tx import tx_sign
from internal.modules.auth.tx import tx_decode, tx_encode
from internal.modules.bank.tx import create_unsigned_txs, tx_send
from modules.auth.query import (
    query_account,
)

HOME = os.getenv("HOME")
DEFAULT_GAS = 2000000


class TestAuthModuleTxsQueries(unittest.TestCase):
    """
    The class `TestAuthModuleTxsQueries` contains test functions
    which test queries of auth module
    """

    def test_query_account(self):
        """
        The function `test_query_account` will query account
        and test balance
        """
        status, key = keys_show("account1", "acc")
        self.assertTrue(status)
        self.assertTrue(key)
        status, _ = query_account(key["address"])
        self.assertTrue(status)

    def test_query_account_fail(self):
        """
        The function `test_query_account_fail` will query wrong account
        and assert fail condition
        """
        status, _ = query_account("cosmos1xpcfd7pxfmv6gd50y9mwjq50kwqpqrh5mmw72h")
        self.assertFalse(status)

    def test_tx_encode(self):
        """
        The function `test_tx_encode` will encode a transaction.
        """
        status, from_account = keys_show("account1", "acc")
        self.assertTrue(status)
        from_address = from_account["address"]
        status, account_resp = query_account(from_address)
        self.assertTrue(status)
        from_address_sequence = account_resp["sequence"]

        status, to_account = keys_show("account2", "acc")
        self.assertTrue(status)
        to_address = to_account["address"]

        status, _ = create_unsigned_txs(
            from_address, to_address, "100stake", "unsigned_tx.json"
        )
        self.assertTrue(status)

        status, signed_tx = tx_sign(
            "unsigned_tx.json", from_address, from_address_sequence, DEFAULT_GAS
        )
        self.assertTrue(status)
        with open(HOME + "/" + "signed_tx.json", "w", encoding="utf8") as outfile:
            json.dump(signed_tx, outfile)
        status, encoded_tx = tx_encode("signed_tx.json")
        self.assertTrue(status)
        status, decoded_json = tx_decode(encoded_tx)
        self.assertTrue(status)
        self.assertEqual(str(signed_tx), str(decoded_json))


if __name__ == "__main__":
    unittest.main()
