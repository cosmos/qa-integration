import tempfile
import time
import logging
import unittest
import inspect
from modules.gov.tx import *  # pylint: disable=W0401,W0614
from modules.gov.query import *  # pylint: disable=W0401
from modules.bank.query import query_balances
from utils import env
from internal.core.keys import keys_show

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

DENOM = env.DENOM
DAEMON_HOME = env.DAEMON_HOME
YES_VOTE = "VOTE_OPTION_YES"
NO_VOTE = "VOTE_OPTION_NO"

validator1_acc = keys_show("validator1", "acc")[1]
validator2_acc = keys_show("validator2", "acc", f"{DAEMON_HOME}-2")[1]
account1 = keys_show("account1", "acc")[1]["address"]

community_spend_amount = 1000
community_spend = f"{community_spend_amount}{DENOM}"
new_tally_quorom = "0.330000000000000000"
upgrade_proposal_name = "upgrade-proposal"
upgrade_proposal_flags = "--title=upgrade --description=upgrade"


class TestGovModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.param_change_file = tempfile.NamedTemporaryFile(  # pylint: disable=R1732
            mode="w+t"
        )
        cls.param_change_file.writelines(
            """{
"title": "Staking Param Change",
"description": "Update max validators",
"changes": [
    {
    "subspace": "gov",
    "key": "tallyparams",
    "value": {"quorum":\""""
            + new_tally_quorom
            + """"}
    }
]
}
        """
        )
        cls.param_change_file.seek(0)

        cls.community_spend_file = tempfile.NamedTemporaryFile(  # pylint: disable=R1732
            mode="w+t"
        )
        cls.community_spend_file.writelines(
            """{
"title": "Community Pool Spend",
"description": "Pay me some Atoms!",
"recipient": \""""
            + account1
            + """",
"amount": \""""
            + community_spend
            + """"
}
        """
        )
        cls.community_spend_file.seek(0)

    def test_software_upgrade_proposal(self):
        self.submit_and_pass_proposal(
            upgrade_proposal_name,
            "software-upgrade",
            extra_args=f"--upgrade-height=12345 {upgrade_proposal_flags}",
        )
        # waiting for proposal to pass
        time.sleep(60)
        self.check_upgrade_plan()

    def test_community_spend_proposal(self):
        status, initial_balance = query_balances(account1, f"--denom {DENOM}")
        self.assertTrue(status, "error when fetching account balance")
        self.submit_and_pass_proposal(
            self.__class__.community_spend_file.name, "community-pool-spend"
        )
        # waiting for proposal to pass
        time.sleep(60)
        status, updated_balance = query_balances(account1, f"--denom {DENOM}")
        self.assertTrue(status, "error when fetching account balance")
        self.assertEqual(
            int(initial_balance["amount"]) + community_spend_amount,
            int(updated_balance["amount"]),
        )

    def test_param_change_proposal(self):
        status, params = query_params()
        self.assertTrue(status, "error when fetching governance params")
        self.assertIsNotNone(params["tally_params"])
        self.assertIsNotNone(params["tally_params"]["quorum"])
        self.assertNotEqual(params["tally_params"]["quorum"], new_tally_quorom)
        # submitting tally quorum param change proposal
        self.submit_and_pass_proposal(
            self.__class__.param_change_file.name, "param-change"
        )
        # waiting for proposal to pass
        time.sleep(60)
        status, tally_param = query_param("tallying")
        self.assertTrue(status, "error when fetching governance tally params")
        self.assertIsNotNone(tally_param["quorum"])
        self.assertEqual(tally_param["quorum"], new_tally_quorom)

    def test_cancel_software_upgrade(self):
        self.check_upgrade_plan()
        # test cancel software upgrade
        self.submit_and_pass_proposal(
            "", "cancel-software-upgrade", extra_args=f"{upgrade_proposal_flags}"
        )
        # waiting for proposal to pass
        time.sleep(60)
        status, plan = query_upgrade_plan()
        if status is False:
            self.assertTrue("no upgrade scheduled" in plan)
        else:
            self.assertIsNotNone(plan["name"])
            self.assertNotEqual(plan["name"], upgrade_proposal_name)

    @classmethod
    def tearDownClass(cls):
        cls.param_change_file.close()
        cls.community_spend_file.close()

    # submit_and_pass_proposal submits proposal and pass it with deposit, vote txs
    def submit_and_pass_proposal(
        self, proposal_file_or_name, proposal_type="software-upgrade", extra_args=""
    ):  # pylint: disable=R0915
        status = True
        # submit proposal
        if proposal_type == "cancel-software-upgrade":
            status, _ = tx_cancel_software_upgrade(
                validator1_acc["name"],
                extra_args=extra_args,
            )
        else:
            status, _ = tx_submit_proposal(
                validator1_acc["name"],
                proposal_file_or_name,
                proposal_type,
                extra_args=extra_args,
            )
        self.assertTrue(status, f"error when executing {proposal_type} proposal")
        time.sleep(4)

        # query all proposals
        status, out = query_proposals()
        self.assertTrue(
            status, f"error when fetching proposals after {proposal_type} proposal"
        )
        proposals = out["proposals"]
        proposals_len = len(proposals)
        self.assertGreaterEqual(proposals_len, 1)

        # query single proposal
        proposal_id = int(proposals[proposals_len - 1]["proposal_id"])
        status, proposal = query_proposal(proposal_id)
        self.assertTrue(status, "error when fetching single proposal")
        self.assertEqual(proposal, proposals[proposals_len - 1])

        status, out = query_proposer(proposal_id)
        self.assertTrue(status, "error when fetching proposer of a proposal")
        self.assertEqual(out["proposer"], validator1_acc["address"])

        # add deposit to a proposal
        deposit_amount = "10000000"
        status, _ = tx_deposit(
            validator1_acc["name"],
            proposal_id,
            deposit_amount + DENOM,
        )
        self.assertTrue(status, "error when depositing to a proposal")
        time.sleep(4)

        # query deposits of a proposal
        status, out = query_deposits(proposal_id)
        self.assertTrue(status, "error when querying deposits of a proposal")
        deposits = out["deposits"]
        self.assertNotEqual(len(deposits), 0)
        self.assertEqual(deposits[0]["depositor"], validator1_acc["address"])
        self.assertNotEqual(deposits[0]["amount"], 0)
        self.assertEqual(deposits[0]["amount"][0]["amount"], deposit_amount)

        # query single deposit
        status, deposit = query_deposit(proposal_id, validator1_acc["address"])
        self.assertTrue(status, "error when querying single deposit of a proposal")
        self.assertEqual(deposit, deposits[0])

        # vote to a proposal
        vote_option = YES_VOTE
        status, out = tx_vote(
            validator1_acc["name"],
            proposal_id,
            vote_option,
        )
        self.assertTrue(status, "error when voting to a proposal")
        time.sleep(4)

        status, out = query_votes(proposal_id)
        self.assertTrue(status, "error when querying votes of a proposal")
        votes = out["votes"]
        self.assertEqual(len(votes), 1)

        # query single vote
        status, vote = query_vote(proposal_id, validator1_acc["address"])
        self.assertTrue(status, "error when querying single vote of a proposal")
        self.assertEqual(vote["voter"], validator1_acc["address"])
        self.assertEqual(vote["option"], vote_option)

        # add weighted-vote to a proposal
        weight_vote_option = f"{YES_VOTE}=0.5,{NO_VOTE}=0.5"
        status, out = tx_weighted_vote(
            validator2_acc["name"],
            proposal_id,
            weight_vote_option,
            home=f"{DAEMON_HOME}-2",
        )
        self.assertTrue(status, "error when weight voting to a proposal")
        time.sleep(4)

        status, out = query_votes(proposal_id)
        self.assertTrue(status, "error when querying votes of a proposal")
        votes = out["votes"]
        self.assertEqual(len(votes), 2)

        # query single vote
        status, vote = query_vote(proposal_id, validator2_acc["address"])
        self.assertTrue(status, "error when querying single weight vote of a proposal")
        self.assertEqual(vote["voter"], validator2_acc["address"])
        self.assertEqual(len(vote["options"]), 2)
        self.assertEqual(vote["options"][0]["option"], YES_VOTE)
        self.assertEqual(vote["options"][1]["option"], NO_VOTE)

        # query tally
        status, tally = query_tally(proposal_id)
        self.assertTrue(status, "error when querying tally of a proposal")
        yes_tally = int(tally["yes"])
        no_tally = int(tally["no"])

        # here we convert tally to weights
        # and check whether yes votes weight is 1.5 and no votes weight is 0.5
        # and remaining options weight is 0
        # as we voted same before
        self.assertEqual(int(tally["abstain"]), 0)
        self.assertEqual(int(tally["no_with_veto"]), 0)
        self.assertEqual(yes_tally * 2 / (yes_tally + no_tally), 1.5)
        self.assertEqual(no_tally * 2 / (yes_tally + no_tally), 0.5)

    def check_upgrade_plan(self):
        status, plan = query_upgrade_plan()
        self.assertTrue(status, "error when fetching upgrade plan")
        self.assertIsNotNone(plan["name"])
        self.assertEqual(plan["name"], upgrade_proposal_name)


if __name__ == "__main__":
    logging.info("INFO: running governance module tests")
    test_src = inspect.getsource(TestGovModule)
    unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: (
        test_src.index(f"def {x}") - test_src.index(f"def {y}")
    )
    unittest.main(verbosity=2)
