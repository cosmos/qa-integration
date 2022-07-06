import tempfile, time, os, logging
from internal.core.keys import keys_show
from modules.gov.tx import *
from modules.gov.query import *

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

DENOM = os.getenv("DENOM")
validator_acc = keys_show("validator1", "acc")[1]
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

logging.info("INFO: running governance module tests")

try:
    # submit software upgrade proposal
    status, proposal = tx_submit_proposal(
        validator_acc["name"],
        "upgrade-proposal",
        "software-upgrade",
        extra_args="--upgrade-height=12345 --title=upgrade --description=upgrade",
    )
    assert status, "error when executing software upgrade proposal"
    time.sleep(3)

    # query all proposals
    status, out = query_proposals()
    assert status, "error when fetching proposals after software upgrade proposal"
    proposals = out["proposals"]
    proposals_len = len(proposals)
    assert proposals_len != 0

    # submit community pool spend proposal
    status, proposal = tx_submit_proposal(
        validator_acc["name"], community_spend_file.name, "community-pool-spend"
    )
    assert status, "error when executing param change proposal"
    time.sleep(3)

    # query all proposals
    status, out = query_proposals()
    assert status, "error when fetching proposals after community spend proposal"
    proposals = out["proposals"]
    assert len(proposals) == (proposals_len + 1)

    # query single proposal
    proposal_id = int(proposals[proposals_len]["proposal_id"])
    status, proposal = query_proposal(proposal_id)
    assert status, "error when fetching single proposal"
    assert proposal == proposals[proposals_len]
    proposals_len += 1

    # add deposit to a proposal
    deposit_amount = "1000"
    status, _ = tx_deposit(
        validator_acc["name"],
        proposal_id,
        deposit_amount + DENOM,
    )
    assert status, "error when depositing to a proposal"
    time.sleep(3)

    # query deposits of a proposal
    status, out = query_deposits(proposal_id)
    assert status, "error when querying deposits of a proposal"
    deposits = out["deposits"]
    assert (
        len(deposits) != 0
        and deposits[0]["depositor"] == validator_acc["address"]
        and len(deposits[0]["amount"]) != 0
        and deposits[0]["amount"][0]["amount"] == deposit_amount
    )

    # query single deposit
    status, deposit = query_deposit(proposal_id, validator_acc["address"])
    assert status, "error when querying single deposit of a proposal"
    assert deposit == deposits[0]

    # submit param change proposal
    status, proposal = tx_submit_proposal(
        validator_acc["name"], param_change_file.name, "param-change"
    )
    assert status, "error when executing param change proposal"
    time.sleep(3)

    # query single proposal
    proposal_id += 1
    proposals_len += 1
    status, proposal = query_proposal(proposal_id)
    assert status, "error when fetching param change proposal"
    assert int(proposal["proposal_id"]) == proposal_id

    logging.info("PASS: all governance module tests")
finally:
    param_change_file.close()
    community_spend_file.close()
