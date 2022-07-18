import os, sys, time, logging
from core.keys import keys_show
from internal.utils import exec_command, env
import tempfile
import unittest
from modules.staking.tx import (
    tx_delegate,
    tx_redelegate,
    tx_unbond,
    tx_create_validator,
)
from modules.staking.query import (
    query_delegator_delegation,
    query_unbonding_delegation,
    query_unbonding_delegations,
    query_validator,
    query_validator_set,
)

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
amount = 5


class TestStakingModuleTxsQueries(unittest.TestCase):

    # delegate tx
    def test_delegate_tx(self):
        status, delegate_tx = tx_delegate("account1", val_addr, amount)
        self.assertTrue(status)
        time.sleep(3)

        # query delegation amount
        before_del_amount = query_delegator_delegation(delegator, val_addr)[1][
            "balance"
        ]["amount"]

        status, delegateTx = tx_delegate("account1", val_addr, amount)
        self.assertTrue(status)
        time.sleep(3)

        # query delegations and match the delagted amount
        after_del_amount = query_delegator_delegation(delegator, val_addr)[1][
            "balance"
        ]["amount"]

        self.assertEqual((int(before_del_amount) + amount), int(after_del_amount))

    # redelegation tx
    def test_redelegate_tx(self):
        status, delegate_tx = tx_delegate("account1", dst_val_address, amount)
        self.assertTrue(status)
        time.sleep(3)

        # query redelegated amount
        before_redel_amount = query_delegator_delegation(delegator, dst_val_address)[
            1
        ]["balance"]["amount"]

        # redelegation tx
        status, redelegate_tx = tx_redelegate(
            "account1", val_addr, dst_val_address, amount
        )
        self.assertTrue(status)
        time.sleep(3)

        # query redelegated amount and match the amount before and after the tx
        after_redel_amount = query_delegator_delegation(delegator, dst_val_address)[1][
            "balance"
        ]["amount"]
        self.assertEqual((int(before_redel_amount) + amount), int(after_redel_amount))

    # unbond tx
    def test_unbond_tx(self):
        status, unbond_tx = tx_unbond("account1", val_addr, amount)
        self.assertTrue(status)
        time.sleep(3)

        # query unbond tx and check the unbonded amount
        status, unbond_amount = query_unbonding_delegation(delegator, val_addr)
        unbond_balance = unbond_amount["entries"][0]["balance"]
        self.assertEqual(amount, int(unbond_balance))

        # query unbond unbond_delegations
        status, unbond_delegations = query_unbonding_delegations(delegator)
        self.assertTrue(status)
        l=len(unbond_delegations)
        self.assertNotEqual(l,0)

    # create validator
    def test_create_validator(self):
        temp_dir = tempfile.TemporaryDirectory()
        temp_dir_name = temp_dir.name
        TEMP_VAL = "validator-10000"

        command = f"{DAEMON} init testvalidator --home {temp_dir_name}"
        tx, tx_err = exec_command(command)
        assert len(tx_err), f"node init failed :: {tx_err}"

        status, create_val_tx = tx_create_validator(
            "account1", amount, TEMP_VAL, temp_dir_name
        )
        self.assertTrue(status)
        time.sleep(3)

        (_, validator) = keys_show("account1", "val")

        # query created validator
        status, validator_res = query_validator(validator["address"])
        self.assertTrue(status)
        val_name = validator_res["description"]["moniker"]
        self.assertEqual(val_name, TEMP_VAL)

        status, validator_set = query_validator_set()
        self.assertTrue(status)
        val_set=len(validator_set)
        self.assertNotEqual(val_set,0)

        # clean tmp dir
        temp_dir.cleanup()


if __name__ == "__main__":
    logging.info("INFO: running staking module tests")
    unittest.main()
