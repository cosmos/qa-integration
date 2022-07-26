import unittest, time
import logging
from modules.upgrade.query import *
from modules.upgrade.tx import *
from utils import exec_command, env

logging.basicConfig(format="%(message)s", level=logging.DEBUG)


upgrade_name = "test_upgrade_tx"
from_key = "validator1"
num_vals = env.NUM_VALS


class TestUpgradeModuleQueries(unittest.TestCase):
    def test_tx_upgrade_proposal(self):
        # query block
        status, block = query_block()
        self.assertTrue(status)
        block_height = int(block["block"]["header"]["height"])
        upgrade_height = block_height + 2000

        # submit proposal
        status, res = tx_submit_proposal(from_key, upgrade_name, upgrade_height)
        self.assertTrue(status)
        time.sleep(3)

        status, proposals = query_proposals()
        self.assertTrue(status)
        l = len(proposals)
        self.assertIsNotNone(l, 0)
        proposal_id = proposals["proposals"][0]["proposal_id"]

        # vote on the proposal
        for i in range(1, int(num_vals)):
            val = f"validator{i}"
            home = f"{DAEMON_HOME}-{i}"
            status, res = tx_vote(val, proposal_id, "yes", home)
            self.assertTrue(status)
            time.sleep(3)

        # waiting for proposal to pass
        time.sleep(60)

        # check if the proposal passed or not
        status, proposal = query_proposal(proposal_id)
        self.assertTrue(status)
        proposal_status = proposal["status"]
        self.assertEqual(proposal_status, "PROPOSAL_STATUS_PASSED")

        # query upgrade plan
        def test_query_upgrade_plan(self):
            # query upgrade plan
            status, plan = query_upgrade_plan()
            self.assertTrue(status)
            self.assertIsNotNone(plan["name"])
            self.assertIsNotNone(plan["height"])

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
