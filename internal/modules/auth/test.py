import unittest

from core.keys import keys_show
from modules.auth.query import (
    query_account,
)

class TestAuthModuleTxsQueries(unittest.TestCase):

    def test_query_account(self):
        status, key = keys_show("account1", "acc")
        print("status", status)
        print("key", key)
        self.assertTrue(status)
        self.assertTrue(key)
        status, response = query_account(key["address"])
        self.assertTrue(status)

    def test_query_account_fail(self):
        status, response = query_account("cosmos1xpcfd7pxfmv6gd50y9mwjq50kwqpqrh5mmw72h")
        self.assertFalse(status)

if __name__ == '__main__':
    unittest.main()
