import logging
import unittest
from modules.params.query import query_subspace
from utils import env

HOME = env.HOME
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

logging.info("INFO :: Running params module tests")


class TestParamsModuleQUeries(unittest.TestCase):
    def test_subspace_query(self):
        status, auth_param = query_subspace("auth", "MaxMemoCharacters")
        self.assertTrue(status)
        max_memo_characters = auth_param["value"]
        self.assertIsNotNone(max_memo_characters)

        status, distribution_param = query_subspace(
            "distribution", "bonusproposerreward"
        )
        self.assertTrue(status)
        bonus_proposer_reward = distribution_param["value"]
        self.assertIsNotNone(bonus_proposer_reward)

        status, staking_param = query_subspace("staking", "MaxValidators")
        self.assertTrue(status)
        max_validators = staking_param["value"]
        self.assertIsNotNone(max_validators)

        status, slashing_param = query_subspace("slashing", "SignedBlocksWindow")
        self.assertTrue(status)
        signed_blocks_window = slashing_param["value"]
        self.assertIsNotNone(signed_blocks_window)


if __name__ == "__main__":
    unittest.main()
