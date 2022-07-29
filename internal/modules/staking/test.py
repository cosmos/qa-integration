"""
This module queries staking sub commands.
"""
import time
import logging
import tempfile
import unittest
from core.keys import keys_show
from modules.staking.tx import *  # pylint: disable=W0401,W0614
from modules.staking.query import *  # pylint: disable=W0401
from internal.utils import exec_command, env

HOME = env.HOME
DAEMON = env.DAEMON
DAEMON_HOME = env.DAEMON_HOME
NODE2_HOME = env.get("NODE2_HOME")
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

# get validator, delegator and dst validator addresses
val_addr = keys_show("validator1", "val")[1]["address"]
delegator = keys_show("account1", "acc")[1]["address"]
dst_val_address = keys_show("validator2", "val", NODE2_HOME)[1]["address"]

# assign the arguments
delegate_amount = 10
redelegation_amount = 6
unbond_amount = 2

temp_dir = tempfile.TemporaryDirectory()  # pylint: disable=R1732
temp_dir_name = temp_dir.name
TEMP_VAL = "validator-10000"


class TestStakingModuleTxsQueries(unittest.TestCase):
    """
    This test case is to test the staking module txs and queries.
    """

    @classmethod
    def setUpClass(cls):

        # delegate tx
        status, _ = tx_delegate("account1", val_addr, delegate_amount)
        assert status, "error in delegate tx!!!"
        time.sleep(3)

        # # redelegation tx
        status, _ = tx_redelegate(
            "account1", val_addr, dst_val_address, redelegation_amount
        )
        assert status, "error in redelegate tx!!!"
        time.sleep(3)

        # unbond tx
        status, _ = tx_unbond("account1", val_addr, unbond_amount)
        assert status, "error in unbond tx!!!"
        time.sleep(3)

        # create validator
        command = f"{DAEMON} init testvalidator --home {temp_dir_name}"
        _, tx_err = exec_command(command)
        assert len(tx_err) != 0, f"node init failed :: {tx_err}"

        status, _ = tx_create_validator(
            "account1", delegate_amount, TEMP_VAL, temp_dir_name
        )
        assert status, "error in create validator tx!!!"
        time.sleep(3)

    def test_delegate_tx(self):

        # query delegation amount
        before_del_amount = query_delegator_delegation(delegator, val_addr)[1][
            "balance"
        ]["amount"]

        status, _ = tx_delegate("account1", val_addr, delegate_amount)
        self.assertTrue(status)
        time.sleep(3)

        # query delegations and match the delagted amount
        after_del_amount = query_delegator_delegation(delegator, val_addr)[1][
            "balance"
        ]["amount"]
        self.assertEqual(
            (int(before_del_amount) + delegate_amount), int(after_del_amount)
        )

    def test_query_delegator_delegations(self):

        # query delegator delegations
        status, delegations = query_delegator_delegations(delegator)
        self.assertTrue(status)
        count = int(delegations["pagination"]["total"])
        self.assertNotEqual(count, 0)

        # query delegations of validator
        status, delegations_of_val = query_delegations_of_validator(val_addr)
        self.assertTrue(status)
        count = int(delegations_of_val["pagination"]["total"])
        self.assertNotEqual(count, 0)

        for d in delegations_of_val["delegation_responses"]:
            del_addr = d["delegation"]["delegator_address"]
            if del_addr == delegator:
                count = 1
                break
        self.assertEqual(count, 1)

    def test_redelegate_tx(self):

        # query redelegated amount
        before_redel_amount = query_delegator_delegation(delegator, dst_val_address)[1][
            "balance"
        ]["amount"]

        # redelegation tx
        status, _ = tx_redelegate(
            "account1", val_addr, dst_val_address, delegate_amount
        )
        self.assertTrue(status)
        time.sleep(3)

        # query redelegated amount and match the amount before and after the tx
        after_redel_amount = query_delegator_delegation(delegator, dst_val_address)[1][
            "balance"
        ]["amount"]
        self.assertEqual(
            (int(before_redel_amount) + delegate_amount), int(after_redel_amount)
        )

    def test_query_delegator_redelegations(self):

        status, _ = query_delegator_redelegation(delegator, val_addr, dst_val_address)
        self.assertTrue(status)

        # query delegator redelegations
        status, redelegations = query_delegator_redelegations(delegator)
        self.assertTrue(status)
        count = int(redelegations["pagination"]["total"])
        self.assertEqual(count, 1)

        # query delegator redelegations from a validator
        status, redelegations_from_val = query_redelegations_from_val(val_addr)
        self.assertTrue(status)
        count = int(redelegations_from_val["pagination"]["total"])
        self.assertEqual(count, 1)

        for r in redelegations_from_val["redelegation_responses"]:
            del_addr = r["redelegation"]["delegator_address"]
            if del_addr == delegator:
                count = 1
                break
        self.assertEqual(count, 1)

    def test_unbond_tx(self):

        # query unbond tx and check the unbonded amount
        status, unbond_tx = query_unbonding_delegation(delegator, val_addr)
        self.assertTrue(status)
        unbond_balance = int(unbond_tx["entries"][0]["balance"])
        self.assertEqual(unbond_balance, unbond_balance)

    def test_query_unbondings(self):

        # query unbond unbond_delegations
        status, unbond_delegations = query_unbonding_delegations(delegator)
        self.assertTrue(status)
        count = int(unbond_delegations["pagination"]["total"])
        self.assertNotEqual(count, 0)

        # query unbond unbond_delegations from a validator
        status, unbond_del_of_val = query_unbondings_from_val(val_addr)
        self.assertTrue(status)
        count = int(unbond_del_of_val["pagination"]["total"])
        self.assertEqual(count, 1)

        for u in unbond_del_of_val["unbonding_responses"]:
            del_addr = u["delegator_address"]
            if del_addr == delegator:
                count = 1
                break
        self.assertEqual(count, 1)

    # create validator
    def test_create_validator(self):

        (_, validator) = keys_show("account1", "val")

        # query created validator
        status, validator_res = query_validator(validator["address"])
        self.assertTrue(status)
        val_name = validator_res["description"]["moniker"]
        self.assertEqual(val_name, TEMP_VAL)

        status, validator_set = query_validator_set()
        self.assertTrue(status)
        count = int(validator_set["pagination"]["total"])
        self.assertEqual(count, 4)

    def test_edit_validator(self):

        (_, validator) = keys_show("account1", "val")
        # edit validator
        status, _ = tx_edit_validator("account1", "temp_val")
        self.assertTrue(status)
        time.sleep(3)

        status, validator_res = query_validator(validator["address"])
        self.assertTrue(status)
        val_name = validator_res["description"]["moniker"]
        self.assertEqual(val_name, "temp_val")

        # clean tmp dir
        temp_dir.cleanup()

    def test_staking_params(self):
        status, staking_params = query_staking_params()
        self.assertTrue(status)
        bond_denom = staking_params["bond_denom"]
        self.assertIsNotNone(bond_denom)

    def test_staking_pool(self):
        status, staking_pool = query_staking_pool()
        self.assertTrue(status)
        bonded_tokens = staking_pool["bonded_tokens"]
        self.assertIsNotNone(bonded_tokens)


if __name__ == "__main__":
    logging.info("INFO: running staking module tests")
    unittest.main()
