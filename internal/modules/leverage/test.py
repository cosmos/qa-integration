import time
import logging
import unittest
import inspect
import pathlib
from internal.modules.gov.tx import submit_and_pass_proposal

from modules.leverage.query import (
    query_registered_tokens,
)

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

class TestLeverageModuleTxsQueries(unittest.TestCase):
    def update_leverage_registry(self):
        update_registry_path = pathlib.Path().resolve().joinpath("./internal/modules/leverage/update-registry-only-umee.json")
        submit_and_pass_proposal(
            proposal_file_or_name=update_registry_path,
            proposal_type='update-registry',
            extra_args='200uumee'
        )
        time.sleep(10)

    def test_query_total_supply(self):
        status, res = query_registered_tokens()
        self.assertTrue(status)

        if len(res['registry']) == 0:
            self.update_leverage_registry()

        status, res = query_registered_tokens()
        self.assertTrue(status)
        self.assertTrue(len(res['registry']) >= 1, "It should have at least one token registered")


if __name__ == "__main__":
    logging.info("INFO: running leverage module tests")
    test_src = inspect.getsource(TestLeverageModuleTxsQueries)
    unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: (
        test_src.index(f"def {x}") - test_src.index(f"def {y}")
    )
    unittest.main(verbosity=2)