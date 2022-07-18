import os, sys, time, logging
from core.keys import keys_show
from internal.utils import DAEMON, exec_command
import tempfile
import unittest
from modules.staking.tx import (
    tx_delegate,
    tx_redelegate,
    tx_unbond,
    tx_create_validator,
)
from modules.staking.query import (
    query_delegator_delegations,
    query_unbonding_delegation,
    query_validator,
)

HOME = os.getenv("HOME")
DAEMON = os.getenv("DAEMON")
DAEMON_HOME = os.getenv("DAEMON_HOME")
NODE2_HOME = os.getenv("NODE_HOME_2")
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

# get validator, delegator and dst validator addresses
validator = keys_show("validator1", "val")[1]["address"]
delegator = keys_show("account1", "acc")[1]["address"]
dst_val_address = keys_show("validator2", "val", NODE2_HOME)[1]["address"]

# assign the arguments
sender, amount_to_be_sent = delegator, 5

if sender == validator:
    sys.exit(
        'Error: The values of arguments "sender" and "receiver" are equal make sure to set different values'
    )


class TestStakingModuleTxsQueries(unittest.TestCase):

    # delegate tx
    def test_delegate_tx(self):
        status, delegate_tx = tx_delegate("account1", validator, amount_to_be_sent)
        self.assertTrue(status)
        time.sleep(3)

        # query delegation amount
        before_del_amount = query_delegator_delegations(delegator, validator)[1][
            "balance"
        ]["amount"]

        status, delegateTx = tx_delegate("account1", validator, amount_to_be_sent)
        self.assertTrue(status)
        time.sleep(3)

        # query delegations and match the delagted amount
        after_del_amount = query_delegator_delegations(delegator, validator)[1][
            "balance"
        ]["amount"]
        assert (int(before_del_amount) + amount_to_be_sent) == int(
            after_del_amount
        ), f"mismatch in delegation amount!!!"

    # redelegation tx
    def test_redelegate_tx(self):
        status, delegate_tx = tx_delegate(
            "account1", dst_val_address, amount_to_be_sent
        )
        self.assertTrue(status)
        time.sleep(3)

        # query redelegated amount
        before_redel_amount = query_delegator_delegations(delegator, dst_val_address)[
            1
        ]["balance"]["amount"]

        # redelegation tx
        status, redelegate_tx = tx_redelegate(
            "account1", validator, dst_val_address, amount_to_be_sent
        )
        self.assertTrue(status)
        time.sleep(3)

        # query redelegated amount and match the amount before and after the tx
        after_redel_amount = query_delegator_delegations(delegator, dst_val_address)[1][
            "balance"
        ]["amount"]
        assert (int(before_redel_amount) + amount_to_be_sent) == int(
            after_redel_amount
        ), f"tx failed! mismatch in redelegation amount!!!"

    # unbond tx
    def test_unbond_tx(self):
        status, unbond_tx = tx_unbond("account1", validator, amount_to_be_sent)
        self.assertTrue(status)
        time.sleep(3)

        # query unbond tx and check the unbonded amount
        status, unbond_amount = query_unbonding_delegation(delegator, validator)
        unbond_balance = unbond_amount["entries"][0]["balance"]
        assert amount_to_be_sent == int(unbond_balance), f"error in unbond tx!!!"

    # create validator
    def test_create_validator(self):
        temp_dir = tempfile.TemporaryDirectory()
        temp_dir_name = temp_dir.name
        TEMP_VAL = "validator-10000"

        command = f"{DAEMON} init testvalidator --home {temp_dir_name}"
        tx, tx_err = exec_command(command)
        assert len(tx_err), f"init tx res :: {tx}"

        status, create_val_tx = tx_create_validator(
            "account1", amount_to_be_sent, TEMP_VAL, temp_dir_name
        )
        self.assertTrue(status)
        time.sleep(3)

        (_, validator) = keys_show("account1", "val")

        # query unbond tx and check the unbonded amount
        status, validator_tx = query_validator(validator["address"])
        self.assertTrue(status)
        val_name = validator_tx["description"]["moniker"]
        assert val_name == TEMP_VAL, f"no validator found with name {TEMP_VAL}"

        # clean tmp dir
        temp_dir.cleanup()


if __name__ == "__main__":
    logging.info("INFO: running staking module tests")
    unittest.main()
    logging.info("PASS: all staking module tests")
