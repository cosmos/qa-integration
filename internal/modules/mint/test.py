import logging,time,json,unittest
from modules.mint.query import *

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

HOME = os.getenv("HOME")
DAEMON_HOME = os.getenv("DAEMON_HOME")

logging.info("INFO :: Running mint module test scripts")

class TestMintModuleQueries(unittest.TestCase):

    def test_params_query(self):
         # query params
        path = f"{HOME}/.simd-1/config/"
        with open(path+'genesis.json') as file:
            data = json.load(file)

        query_param = query_params()[1]

        assert (data["app_state"]["mint"]["params"] == query_param), f"missmatch in params"
        time.sleep(3)

    def test_inflation_query(self):
        status,inflation = query_inflation()
        assert status, f"Querying minting inflation was failed"
        time.sleep(3)

    def test_annual_provision_query(self):
        status,provision = query_annual_provision()
        assert status, f"Querying minting annual provision was failed"
        time.sleep(3)

if __name__ == '__main__':
    unittest.main() 