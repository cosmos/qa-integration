import time
import logging
import unittest
import inspect
import pathlib
from internal.modules.gov.tx import submit_and_pass_proposal

from modules.oracle.query import (
    query_params,
)

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

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


if __name__ == "__main__":
    logging.info("INFO: running oracle module tests")
    test_src = inspect.getsource(TestOracleModule)
    unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: (
        test_src.index(f"def {x}") - test_src.index(f"def {y}")
    )
    unittest.main(verbosity=2)
