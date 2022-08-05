"""
This module contains all auth test functions.
"""
import unittest

from core.keys import keys_show
from modules.auth.query import (
    query_account,
)


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
        status, _ = query_account("umee1xpcfd7pxfmv6gd50y9mwjq50kwqpqrh5mmw72h")
        self.assertFalse(status)


if __name__ == "__main__":
    unittest.main()
