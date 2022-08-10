import time
import logging
import unittest
import inspect
import pathlib
from internal.modules.gov.tx import submit_and_pass_proposal
from internal.modules.oracle.query import query_aggregate_prevote
from utils import env
from internal.core.keys import keys_show

from modules.oracle.query import (
    query_params,
)

from modules.oracle.tx import (
    tx_submit_prevote
)

from modules.oracle.utils import (
    get_hash
)

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

STATIC_EXCHANGE_RATES = "UMEE:0.02,ATOM:1.00,JUNO:0.50"
STATIC_SALT = "af8ed1e1f34ac1ac00014581cbc31f2f24480b09786ac83aabf2765dada87509"

validator1_home = f"{env.DAEMON_HOME}-1"
validator2_home = f"{env.DAEMON_HOME}-2"

validator1_acc = keys_show("validator1", "val")[1]
validator2_acc = keys_show("validator2", "val", validator2_home)[1]

class TestOracleModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        update_params = pathlib.Path().resolve().joinpath("./internal/modules/oracle/update-params.json")
        submit_and_pass_proposal(
            proposal_file_or_name=update_params,
            proposal_type='param-change'
        )

    def test_query_oracle_params(self):
        status, res = query_params()
        self.assertTrue(status)
        self.assertTrue(len(res['params']['accept_list']) >= 1, "It should have at least one token in the accept list")

    # test_prevotes tests to make sure that we can submit prevotes
    def test_prevotes(self):
        # Get Hash
        vote_hash_1 = get_hash(STATIC_EXCHANGE_RATES, STATIC_SALT, validator1_acc["address"])
        vote_hash_2 = get_hash(STATIC_EXCHANGE_RATES, STATIC_SALT, validator2_acc["address"])
        # Submit 1st prevote
        status = tx_submit_prevote(validator1_acc["name"], vote_hash_1, validator1_home)
        self.assertTrue(status)
        time.sleep(1)
        # Submit 2nd prevote
        status = tx_submit_prevote(validator2_acc["name"], vote_hash_2, validator2_home)
        self.assertTrue(status)
        time.sleep(1)

        # Query to verify prevotes exist
        status, prevote_1 = query_aggregate_prevote(validator1_acc["address"])
        self.assertTrue(status)
        self.assertEqual(prevote_1["hash"], vote_hash_1)
        status, prevote_2 = query_aggregate_prevote(validator2_acc["address"])
        self.assertTrue(status)
        self.assertEqual(prevote_2["hash"], vote_hash_2)

    # test_hash makes sure our hasher is accurate
    def test_hash(self):
        hash = get_hash("ATOM:11.1,USDT:1.00001", "salt", "umeevaloper1zypqa76je7pxsdwkfah6mu9a583sju6xjettez")
        self.assertEqual(hash, "A8CFF0088F7D32230AAAE3BC4E55AAB8EDB30732")

if __name__ == "__main__":
    logging.info("INFO: running oracle module tests")
    test_src = inspect.getsource(TestOracleModule)
    unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: (
        test_src.index(f"def {x}") - test_src.index(f"def {y}")
    )
    unittest.main(verbosity=2)
