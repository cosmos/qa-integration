import time, logging, json
import unittest
from utils import exec_command, env
from core.keys import keys_show
from modules.staking.query import query_validator, fetch_validator_pubkey_from_node
from modules.slashing.query import *
from modules.slashing.tx import (
    tx_unjail,
)

HOME = env.HOME
NODE2_HOME = env.get("NODE2_HOME")
NODE3_HOME = env.get("NODE3_HOME")

cmd = f"sudo -S systemctl stop simd-3"
exec_command(cmd)
time.sleep(5)

validator = keys_show("validator3", "val", NODE3_HOME)[1]["address"]
consensus_pubkey = fetch_validator_pubkey_from_node(NODE2_HOME)[1]

logging.basicConfig(format="%(message)s", level=logging.DEBUG)


class TestStakingModuleTxsQueries(unittest.TestCase):
    def test_unjain_tx(self):

        cmd = f"sudo -S systemctl start simd-3"
        exec_command(cmd)
        time.sleep(5)

        # unjain tx
        status, send_tx = tx_unjail("validator3")
        self.assertTrue(status)
        time.sleep(15)

        status = query_validator(validator)[1]["jailed"]
        self.assertFalse(status, "validator unjail tx falied")

    def test_params_query(self):
        # query params
        path = f"{HOME}/.simd-1/config/"
        with open(path + "genesis.json") as file:
            data = json.load(file)
        query_param = query_params()[1]

        assert (
            data["app_state"]["slashing"]["params"] == query_param
        ), "missmatch in params"
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


if __name__ == "__main__":
    logging.info("INFO: running slashing module tests")
    unittest.main()
