import tempfile, time, os, logging
from internal.core.keys import keys_show
from modules.gov.tx import *
from modules.gov.query import *
from utils import env

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

DENOM = env.DENOM
DAEMON_HOME = env.DAEMON_HOME
YES_VOTE = "VOTE_OPTION_YES"
NO_VOTE = "VOTE_OPTION_NO"

validator1_acc = keys_show("validator1", "acc")[1]
validator2_acc = keys_show("validator2", "acc", f"{DAEMON_HOME}-2")[1]
account1 = keys_show("account1", "acc")[1]

param_change_file = tempfile.NamedTemporaryFile()
param_change_file.write(
    b"""{
  "title": "Staking Param Change",
  "description": "Update max validators",
  "changes": [
    {
      "subspace": "staking",
      "key": "MaxValidators",
      "value": 105
    }
  ]
}
"""
)
param_change_file.seek(0)

community_spend_file = tempfile.NamedTemporaryFile(mode="w+t")
community_spend_file.writelines(
    """{
  "title": "Community Pool Spend",
  "description": "Pay me some Atoms!",
  "recipient": "cosmos1s5afhd6gxevu37mkqcvvsj8qeylhn0rz46zdlq",
  "amount": "1000"""
    + DENOM
    + """"
}
"""
)
community_spend_file.seek(0)

# submit_and_pass_proposal submits proposal and pass it with deposit, vote txs
def submit_and_pass_proposal(
    proposal_file_or_name, proposal_type="software-upgrade", extra_args=""
):
    # submit community pool spend proposal
    status, proposal = tx_submit_proposal(
        validator1_acc["name"],
        proposal_file_or_name,
        proposal_type,
        extra_args=extra_args,
    )
    assert status, f"error when executing {proposal_type} proposal"
    time.sleep(4)

    # query all proposals
    status, out = query_proposals()
    assert status, f"error when fetching proposals after {proposal_type} proposal"
    proposals = out["proposals"]
    proposals_len = len(proposals)
    assert proposals_len >= 1

    # query single proposal
    proposal_id = int(proposals[proposals_len - 1]["proposal_id"])
    status, proposal = query_proposal(proposal_id)
    assert status, "error when fetching single proposal"
    assert proposal == proposals[proposals_len - 1]

    status, out = query_proposer(proposal_id)
    assert status, "error when fetching proposer of a proposal"
    assert out["proposer"] == validator1_acc["address"]

    # add deposit to a proposal
    deposit_amount = "10000000"
    status, _ = tx_deposit(
        validator1_acc["name"],
        proposal_id,
        deposit_amount + DENOM,
    )
    assert status, "error when depositing to a proposal"
    time.sleep(4)

    # query deposits of a proposal
    status, out = query_deposits(proposal_id)
    assert status, "error when querying deposits of a proposal"
    deposits = out["deposits"]
    assert len(deposits) != 0
    assert deposits[0]["depositor"] == validator1_acc["address"]
    assert len(deposits[0]["amount"]) != 0
    assert deposits[0]["amount"][0]["amount"] == deposit_amount

    # query single deposit
    status, deposit = query_deposit(proposal_id, validator1_acc["address"])
    assert status, "error when querying single deposit of a proposal"
    assert deposit == deposits[0]

    # vote to a proposal
    vote_option = YES_VOTE
    status, out = tx_vote(
        validator1_acc["name"],
        proposal_id,
        vote_option,
    )
    assert status, "error when voting to a proposal"
    time.sleep(4)

    status, out = query_votes(proposal_id)
    assert status, "error when querying votes of a proposal"
    votes = out["votes"]
    assert len(votes) == 1
    assert votes[0]["voter"] == validator1_acc["address"]
    assert votes[0]["option"] == vote_option

    # query single vote
    status, vote = query_vote(proposal_id, validator1_acc["address"])
    assert status, "error when querying single vote of a proposal"
    assert vote == votes[0]

    # add weighted-vote to a proposal
    weight_vote_option = f"{YES_VOTE}=0.5,{NO_VOTE}=0.5"
    status, out = tx_weighted_vote(
        validator2_acc["name"], proposal_id, weight_vote_option, home=f"{DAEMON_HOME}-2"
    )
    assert status, "error when weight voting to a proposal"
    time.sleep(4)

    status, out = query_votes(proposal_id)
    assert status, "error when querying votes of a proposal"
    votes = out["votes"]
    assert len(votes) == 2
    assert votes[1]["voter"] == validator2_acc["address"]
    assert len(votes[1]["options"]) == 2
    assert votes[1]["options"][0]["option"] == YES_VOTE
    assert votes[1]["options"][1]["option"] == NO_VOTE

    # query single vote
    status, vote = query_vote(proposal_id, validator2_acc["address"])
    assert status, "error when querying single weight vote of a proposal"
    assert vote == votes[1]

    # query tally
    status, tally = query_tally(proposal_id)
    assert status, "error when querying tally of a proposal"
    yes_tally = int(tally["yes"])
    no_tally = int(tally["no"])
    # here we convert tally to weights
    # and check whether yes votes weight is 1.5 and no votes weight is 0.5
    # and remaining options weight is 0
    # as we voted same before
    assert int(tally["abstain"]) == 0
    assert int(tally["no_with_veto"]) == 0
    assert yes_tally * 2 / (yes_tally + no_tally) == 1.5
    assert no_tally * 2 / (yes_tally + no_tally) == 0.5


logging.info("INFO: running governance module tests")
try:
    submit_and_pass_proposal(
        "upgrade-proposal",
        "software-upgrade",
        extra_args="--upgrade-height=12345 --title=upgrade --description=upgrade",
    )

    submit_and_pass_proposal(community_spend_file.name, "community-pool-spend")

    submit_and_pass_proposal(param_change_file.name, "param-change")

    logging.info("PASS: all governance module tests")
finally:
    param_change_file.close()
    community_spend_file.close()
