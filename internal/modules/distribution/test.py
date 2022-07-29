import logging
import time
import unittest
from core.keys import keys_show
from modules.distribution.tx import (
    tx_fund_communitypool,
    tx_set_withdraw_addr,
    tx_withdraw_allrewards,
    tx_withdraw_commision_rewards,
    tx_withdraw_rewards,
)
from modules.distribution.query import (
    query_commission_rewards,
    query_community_pool,
    query_params,
    query_rewards,
    query_rewards_singleval,
    query_slashes,
    query_validator_outstanding_rewards,
)
from modules.bank.query import query_balances
from modules.staking.tx import tx_delegate
from internal.utils import exec_command, env

HOME = env.HOME
DAEMON_HOME = env.DAEMON_HOME
NODE2_HOME = env.get("NODE2_HOME")
NODE3_HOME = env.get("NODE3_HOME")
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

validator1 = keys_show("validator1", "val")[1]["address"]
validator2 = keys_show("validator2", "val", NODE2_HOME)[1]["address"]
validator3 = keys_show("validator3", "val", NODE3_HOME)[1]["address"]
delegator1 = keys_show("account1", "acc")[1]["address"]
delegator2 = keys_show("account2", "acc")[1]["address"]

amount_to_be_sent = 100

cmd = "sudo -S systemctl stop simd-3"
exec_command(cmd)

logging.info("INFO :: Running distribution module tests")

tx_status, delegate_tx = tx_delegate("account1", validator1, amount_to_be_sent)
assert tx_status, f"error in delegate tx: {delegate_tx}"
time.sleep(10)

tx_status, delegate_tx = tx_delegate("account1", validator2, amount_to_be_sent)
assert tx_status, f"error in delegate tx: {delegate_tx}"
time.sleep(10)


class TestDistributionModuleTxsQueries(unittest.TestCase):
    def test_withdraw_rewards_tx(self):
        # query balance
        before_balance = query_balances(delegator1)[1]["balances"][0]["amount"]
        # query rewards
        rewards = query_rewards_singleval(delegator1, validator1)[1]["rewards"][0][
            "amount"
        ]

        # withdraw rewards tx
        status, rewards_tx = tx_withdraw_rewards("account1", validator1)
        self.assertTrue(status)
        self.assertTrue(rewards_tx)
        time.sleep(3)

        # query balance
        after_balance = query_balances(delegator1)[1]["balances"][0]["amount"]

        self.assertEqual(
            (int(before_balance) + int(float(rewards))), int(after_balance)
        )
        time.sleep(5)

    def test_withdraw_all_rewards_tx(self):
        # query balance
        before_balance = query_balances(delegator1)[1]["balances"][0]["amount"]
        # query all rewards
        all_rewards = query_rewards(delegator1)[1]["rewards"]
        total = 0
        for x in all_rewards:
            rewards = x["reward"][0]["amount"]
            total = total + (float(rewards))

        # tx withdraw all rewards
        status, all_rewards = tx_withdraw_allrewards("account1")
        self.assertTrue(status)
        self.assertTrue(all_rewards)

        after_balance = query_balances(delegator1)[1]["balances"][0]["amount"]
        self.assertEqual(
            (int(before_balance) + int(total)), int(after_balance)
        )
        time.sleep(3)

    def test_fund_community_pool_tx(self):
        # fund community pool tx
        status, fund_pool = tx_fund_communitypool("account1", amount_to_be_sent)
        self.assertTrue(status)
        self.assertTrue(fund_pool)

        # query community pool fund
        pool_fund = query_community_pool()[1]["pool"][0]["amount"]
        time.sleep(5)

        # fund community pool tx
        status, fund_pool = tx_fund_communitypool("account1", amount_to_be_sent)
        self.assertTrue(status)
        self.assertTrue(fund_pool)
        time.sleep(5)

        after_pool_fund = query_community_pool()[1]["pool"][0]["amount"]
        self.assertLess(float(pool_fund), float(after_pool_fund))
        time.sleep(3)

    def test_set_withdraw_address_tx(self):
        # tx set withdraw address
        status, set_addr = tx_set_withdraw_addr("account1", delegator2)
        self.assertTrue(status)
        self.assertTrue(set_addr)

        # query balance
        before_balance = query_balances(delegator2)[1]["balances"][0]["amount"]
        # query rewards
        before_reward = query_rewards_singleval(delegator1, validator1)[1]["rewards"][
            0
        ]["amount"]

        # tx withdraw rewards
        status, rewards = tx_withdraw_rewards("account2", validator1)
        self.assertTrue(status)
        self.assertTrue(rewards)

        # query balance
        after_balance = query_balances(delegator2)[1]["balances"][0]["amount"]
        assert int(after_balance) == int(before_balance) + int(
            float(before_reward)
        ), "Set withdraw rewards tx failed"
        time.sleep(3)

    def test_params_query(self):
        status, distribution_params = query_params()
        self.assertTrue(status)
        base_prposer_reward = distribution_params["base_proposer_reward"]
        self.assertIsNotNone(base_prposer_reward)
        community_tax = distribution_params["community_tax"]
        self.assertIsNotNone(community_tax)
        time.sleep(5)

    def test_commission_rewards_tx(self):
        # withdraw commission rewards
        status, commission_rewards = tx_withdraw_commision_rewards(
            "validator1", validator1
        )
        self.assertTrue(status)
        self.assertTrue(commission_rewards)
        time.sleep(10)

        # query commission rewards
        rewards = query_commission_rewards(validator1)[1]["commission"][0]["amount"]

        #time.sleep(3)
        status, commission_rewards = tx_withdraw_commision_rewards(
            "validator1", validator1
        )
        self.assertTrue(status)
        self.assertTrue(commission_rewards)
        time.sleep(3)

        after_rewards = query_commission_rewards(validator1)[1]["commission"][0][
            "amount"
        ]
        self.assertLess(
            float(after_rewards), float(rewards)
        )
        time.sleep(3)

    def test_validator_slashes_query(self):
        # query validator slashes
        slash_count = query_slashes(validator3, 1, 1000)[1]["slashes"]
        self.assertNotEqual(slash_count, 0)
        time.sleep(3)

    def test_validator_outstanding_rewards_query(self):
        # Query validator outstanding rewards
        outstanding_rewards = query_validator_outstanding_rewards(validator1)[1][
            "rewards"
        ][0]["amount"]
        self.assertNotEqual(
            outstanding_rewards, 0, "missmatch in validator outstanding rewards"
        )
        time.sleep(3)


if __name__ == "__main__":
    unittest.main()
