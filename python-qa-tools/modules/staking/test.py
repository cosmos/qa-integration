import os, sys, time, logging
from core.keys import keys_show
from modules.staking.tx import (
    tx_delegate,
    tx_redelegate,
    tx_unbond,
    tx_create_validator,
)
from modules.staking.query import (
    query_all_redelegations,
    query_staking_delegations,
    query_staking_redelegation,
    query_unbonding_delegation,
)

HOME = os.getenv("HOME")
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

# get validator, delegator and dst validator address
validator = keys_show("validator1", "val", 1)[1]["address"]
delegator = keys_show("account1", "acc", 1)[1]["address"]
dst_val_address = keys_show("validator2", "val", 2)[1]["address"]

# assign the arguments
sender, amount_to_be_sent = delegator, 5

if sender == validator:
    sys.exit(
        'Error: The values of arguments "sender" and "receiver" are equal make sure to set different values'
    )

# delegate tx
status, delegate_tx = tx_delegate("account1", validator, amount_to_be_sent)
if not status:
    logging.error(f"error in delegation tx :: {delegate_tx}")
else:
    logging.info(f"tx_hash of delegate_tx :: {delegate_tx['txhash']}")

time.sleep(3)

# query delegation amount
before_del_amount = query_staking_delegations(delegator, validator)[1]["balance"][
    "amount"
]

status, delegateTx = tx_delegate("account1", validator, amount_to_be_sent)
if not status:
    logging.error(f"{delegateTx}")
else:
    logging.info(f"tx_hash to :: {delegateTx['txhash']}")

time.sleep(3)

# query delegations and match the delagted amount
after_del_amount = query_staking_delegations(delegator, validator)[1]["balance"][
    "amount"
]
if (int(before_del_amount) + amount_to_be_sent) == int(after_del_amount):
    logging.info(f"delegation tx was successfull from {delegator} to {validator}")
else:
    logging.error("mismatch in delegation amount...")

# redelegation tx
status, delegateTx = tx_delegate("account1", dst_val_address, amount_to_be_sent)
if not status:
    logging.error(f"{delegateTx}")
else:
    logging.info(f"tx_hash if delegate_tx :: {delegateTx['txhash']}")

time.sleep(3)

# query redelegation amount
before_redel_amount = query_staking_delegations(delegator, dst_val_address)[1][
    "balance"
]["amount"]

# redelegation tx
status, redelegateTx = tx_redelegate(
    "account1", validator, dst_val_address, amount_to_be_sent
)
if not status:
    logging.error(f"redelegation tx status :: {status}")
else:
    logging.info(f"tx_hash of redelegate tx :: {redelegateTx['txhash']}")

time.sleep(3)

# query redelegation amount and match the amount before and after the tx
after_redel_amount = query_staking_delegations(delegator, dst_val_address)[1][
    "balance"
]["amount"]
if (int(before_redel_amount) + amount_to_be_sent) == int(after_redel_amount):
    logging.info(
        f"redelegation tx was successfull from {delegator} to {dst_val_address}"
    )
else:
    logging.error("mismatch in redelegation amount...")


# unbond tx
status, unbond_tx = tx_unbond("account1", validator, amount_to_be_sent)
if not status:
    logging.error(f"unbond tx status :: {status}")
else:
    logging.info(f"unbond tx :: {unbond_tx['txhash']}")

time.sleep(3)

# query unbond tx and check the unbonded amount
status, unbond_amount = query_unbonding_delegation(delegator, validator)
unbond_balance = unbond_amount["entries"][0]["balance"]
if amount_to_be_sent == int(unbond_balance):
    logging.info(f"unbonding tx is successfull..")
else:
    logging.error("error in unbond tx.")
