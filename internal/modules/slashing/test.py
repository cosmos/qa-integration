import time
import logging
import json
import unittest
from utils import exec_command, env
from core.keys import keys_show
from modules.staking.query import query_validator, fetch_validator_pubkey_from_node
from modules.slashing.query import query_params, query_signing_info, query_signing_infos
from modules.slashing.tx import (
    tx_unjail,
)

HOME = env.HOME
NUM_VALS = int(env.NUM_VALS)
NODE2_HOME = env.get("NODE2_HOME")

consensus_pubkey = fetch_validator_pubkey_from_node(NODE2_HOME)[1]

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

if NUM_VALS < 3:
    logging.error(f"""{NUM_VALS} nodes are not enough to test slashing module tests""")
else:
    NODE3_HOME = env.get("NODE3_HOME")
    validator = keys_show("validator3", "val", NODE3_HOME)[1]["address"]
    cmd = "sudo -S systemctl stop simd-3"
    exec_command(cmd)
    time.sleep(20)

    class TestStakingModuleTxsQueries(unittest.TestCase):
        def test_params_query(self):
            # query params
            status, slashing_params = query_params()
            self.assertTrue(status)
            signed_blocks_window = slashing_params["signed_blocks_window"]
            self.assertIsNotNone(signed_blocks_window)
            time.sleep(3)

        def test_signing_infos_query(self):
            # query signing infos
            status, signing_infos = query_signing_infos()
            self.assertTrue(status)
            self.assertIsNotNone(signing_infos, "signing-infos query failed")
            time.sleep(3)

        def test_signing_info_query(self):
            # query validator signing info
            public_key = json.dumps(consensus_pubkey, separators=(",", ":"))
            status, signing_info = query_signing_info(public_key)
            self.assertTrue(status)
            self.assertIsNotNone(signing_info, "validator signing-info query failed")
            time.sleep(3)

        def test_unjail_tx(self):
            time.sleep(5)
            status = query_validator(validator)[1]["jailed"]
            self.assertTrue(status)
            start_chain_cmd = "sudo -S systemctl start simd-3"
            exec_command(start_chain_cmd)
            time.sleep(20)

            # unjain tx
            status, _ = tx_unjail("validator3")
            self.assertTrue(status)
            time.sleep(20)

            status = query_validator(validator)[1]["jailed"]
            self.assertFalse(status, "validator unjail tx has falied")

    if __name__ == "__main__":
        logging.info("INFO: running slashing module tests")
        unittest.main()
