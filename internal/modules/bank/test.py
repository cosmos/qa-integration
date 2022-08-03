import time
import logging
import unittest
from core.keys import keys_show
from modules.bank.tx import (
    tx_send,
)
from modules.bank.query import (
    query_balances,
    query_total_suply,
)

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

sender = keys_show("account1")[1]["address"]
receiver = keys_show("account2")[1]["address"]

# assign the arguments
amount = 5

if sender == receiver:
    logging.error(
        "Error: The values of arguments sender and \
receiver are equal make sure to set different values"
    )


class TestBankModuleTxsQueries(unittest.TestCase):
    def test_send_tx(self):
        # Fetch balances of sender and receiver accounts before executing the send_tx
        status, sender_balance_old = query_balances(sender)
        self.assertTrue(status)
        sender_balance_old = int(sender_balance_old["balances"][0]["amount"])

        # Fetch balances of receiver
        status, receiver_balance_old = query_balances(receiver)
        self.assertTrue(status)
        receiver_balance_old = int(receiver_balance_old["balances"][0]["amount"])

        # send tx
        status, send_tx = tx_send(sender, receiver, amount)
        self.assertTrue(status, send_tx)
        time.sleep(3)

        # Fetch new balances of sender and receiver accounts after executing send_tx
        status, sender_balance_new = query_balances(sender)
        self.assertTrue(status)
        sender_balance_new = int(sender_balance_new["balances"][0]["amount"])

        # Fetch balances of receiver
        status, receiver_balance_new = query_balances(receiver)
        self.assertTrue(status)
        receiver_balance_new = int(receiver_balance_new["balances"][0]["amount"])

        self.assertEqual((sender_balance_old - amount), sender_balance_new)
        self.assertEqual((receiver_balance_old + amount), receiver_balance_new)

    def test_query_total_supply(self):
        # test total supply
        status, res = query_total_suply()
        self.assertTrue(status)
        toatl_supply = res["amount"]
        self.assertIsNotNone(toatl_supply)


if __name__ == "__main__":
    logging.info("INFO: running bank module tests")
    unittest.main()
