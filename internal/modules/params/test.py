import logging
import json
import unittest
from modules.params.query import query_subspace
from utils import env

HOME = env.HOME
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

logging.info("INFO :: Running params module tests")


class TestParamsModuleQUeries(unittest.TestCase):
    def test_subspace_query(self):
        path = f"{HOME}/.simd-1/config/"
        with open(path + "genesis.json",encoding="utf8") as file:
            data = json.load(file)

        # query auth param key
        subspace_auth = query_subspace("auth", "MaxMemoCharacters")[1]["value"]
        self.assertEqual(
            eval(subspace_auth),
            (data["app_state"]["auth"]["params"]["max_memo_characters"]),
            "missmatch in auth pramas",
        )

        # query distribution param key
        subspace_distribution = query_subspace("distribution", "bonusproposerreward")[
            1
        ]["value"]
        self.assertEqual(
            eval(subspace_distribution),
            (data["app_state"]["distribution"]["params"]["bonus_proposer_reward"]),
            "missmatch in distribution pramas",
        )

        # query staking param key
        subspace_staking = query_subspace("staking", "MaxValidators")[1]["value"]
        self.assertEqual(
            eval(subspace_staking),
            (data["app_state"]["staking"]["params"]["max_validators"]),
            "missmatch in staking pramas",
        )

        # query slashing param key
        subspace_slashing = query_subspace("slashing", "SignedBlocksWindow")[1]["value"]
        self.assertEqual(
            eval(subspace_slashing),
            (data["app_state"]["slashing"]["params"]["signed_blocks_window"]),
            "missmatch in slashing pramas",
        )


if __name__ == "__main__":
    unittest.main()
