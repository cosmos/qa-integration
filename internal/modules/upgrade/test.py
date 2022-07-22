import unittest
import logging
from modules.upgrade.query import *

logging.basicConfig(format="%(message)s", level=logging.DEBUG)


class TestUpgradeModuleQueries(unittest.TestCase):
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
