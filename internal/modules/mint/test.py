import logging
import time
import json
import unittest
from modules.mint.query import(
    query_annual_provision, 
    query_inflation, 
    query_params
)
from internal.utils import env

HOME = env.HOME
DAEMON_HOME = env.DAEMON_HOME
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

logging.info("INFO :: Running mint module test scripts")


class TestMintModuleQueries(unittest.TestCase):
    def test_params_query(self):
        # query params
        path = f"{HOME}/.simd-1/config/"
        with open(path + "genesis.json",encoding="utf8") as file:
            data = json.load(file)

        query_param = query_params()[1]

        assert data["app_state"]["mint"]["params"] == query_param, "missmatch in params"
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
