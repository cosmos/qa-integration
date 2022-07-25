import logging
import time
import unittest
from modules.mint.query import query_annual_provision, query_inflation, query_params
from internal.utils import env

HOME = env.HOME
DAEMON_HOME = env.DAEMON_HOME
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

logging.info("INFO :: Running mint module test scripts")


class TestMintModuleQueries(unittest.TestCase):
    def test_params_query(self):
        status, mint_params = query_params()
        self.assertTrue(status)
        inflation_min = mint_params["inflation_min"]
        self.assertIsNotNone(inflation_min)
        goal_bonded = mint_params["goal_bonded"]
        self.assertIsNotNone(goal_bonded)
        time.sleep(3)

    def test_inflation_query(self):
        status, inflation = query_inflation()
        self.assertTrue(status)
        self.assertGreaterEqual(inflation, 0, "Querying minting inflation was failed")
        time.sleep(3)

    def test_annual_provision_query(self):
        status, provision = query_annual_provision()
        self.assertTrue(status)
        self.assertIsNotNone(provision, "Querying minting annual provision was failed")
        time.sleep(3)


if __name__ == "__main__":
    unittest.main()
