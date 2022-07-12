import unittest

from core.keys import keys_show
from modules.auth.query import (
    query_account,
)

class TestStringMethods(unittest.TestCase):

    def test_query_account(self):
        address = keys_show("account1", "acc")[1]["address"]
        status, response = query_account(address)
        self.assertTrue(status)

    def test_query_account_fail(self):
        address = keys_show("cosmos1xpcfd7pxfmv6gd50y9mwjq50kwqpqrh5mmw72h")
        status, response = query_account(address)
        self.assertFalse(status)

if __name__ == '__main__':
    unittest.main()