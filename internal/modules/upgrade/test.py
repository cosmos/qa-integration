import unittest, time
import logging
from modules.upgrade.query import *
from modules.upgrade.tx import *
from utils import exec_command, env

logging.basicConfig(format="%(message)s", level=logging.DEBUG)


upgrade_name = "test_upgrade_tx"
from_key = "validator1"
upgrade_height = ""
num_vals = env.NUM_VALS


class TestUpgradeModuleQueries(unittest.TestCase):
    def test_tx_upgrade_proposal(self):
        status, block = query_block()
        self.assertTrue(status)
        # b = block["block"]["header"]
        block_height = int(block["block"]["header"]["height"])
        print(f"block height.........{block_height}")
        upgrade_height = block_height + 80

        status, res = tx_submit_proposal(from_key, upgrade_name, upgrade_height)
        self.assertTrue(status)
        time.sleep(3)
        # print(f"status and res...........{status} {res}")

        status, proposals = query_proposals()
        self.assertTrue(status)
        print(f"proposalsssssss........{proposals}")
        proposal_id = proposals["proposals"][0]["proposal_id"]

        print(f"iiiiiiiii.............{num_vals} ")
        for i in range(1, int(num_vals)):
            print(f"iiiiiiiii.............validator{i} ")
            val = f"validator{i}"
            home=f"{DAEMON_HOME}-{i}"
            print(f"home...............{home}")
            status, res = tx_vote(val, proposal_id, "yes", home)
            self.assertTrue(status)
            time.sleep(3)

        time.sleep(60)

        print(f"waiting for upgrade.....")
        # time.sleep(10)

        status, proposals = query_proposals()
        self.assertTrue(status)
        print(f"proposalsssssss status after upgrade........{proposals}, {proposals}")

    # query module versions
    def test_query_module_version(self):
        status, modules_versions = query_module_versions()
        self.assertTrue(status)
        l = len(modules_versions["module_versions"])
        self.assertNotEqual(l, 0)
        for module in modules_versions["module_versions"]:
            module_name = module["name"]
            self.assertIsNotNone(module_name)
            status, version_res = query_module_version(module_name)
            self.assertTrue(status)
            version = version_res["module_versions"][0]["version"]
            self.assertIsNotNone(version)
            v = module["version"]
            self.assertEqual(version, v)


if __name__ == "__main__":
    logging.info("INFO: running upgrade module tests")
    unittest.main()
