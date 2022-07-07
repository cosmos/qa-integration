import os, sys, time, logging
from core.keys import keys_show
from internal.utils import DAEMON, exec_command
import tempfile
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
os.environ["node1_home"] = f"{DAEMON_HOME}-1"
os.environ["node2_home"] = f"{DAEMON_HOME}-2"
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

# get validator, delegator and dst validator addresses
node2_home = os.getenv("node2_home")
validator = keys_show("validator1", "val")[1]["address"]
delegator = keys_show("account1", "acc")[1]["address"]
dst_val_address = keys_show("validator2", "val", node2_home)[1]["address"]

# assign the arguments
sender, amount_to_be_sent = delegator, 5

if sender == validator:
    sys.exit(
        'Error: The values of arguments "sender" and "receiver" are equal make sure to set different values'
    )

# delegate tx
status, delegate_tx = tx_delegate("account1", validator, amount_to_be_sent)
assert status, f"error in delegation tx :: {delegate_tx}"
time.sleep(3)

# query delegation amount
before_del_amount = query_delegator_delegations(delegator, validator)[1]["balance"][
    "amount"
]

status, delegateTx = tx_delegate("account1", validator, amount_to_be_sent)
assert status, f"error in delegation tx :: {delegate_tx}"
time.sleep(3)

# query delegations and match the delagted amount
after_del_amount = query_delegator_delegations(delegator, validator)[1]["balance"][
    "amount"
]
if (int(before_del_amount) + amount_to_be_sent) == int(after_del_amount):
    logging.info(f"delegation tx was successfull from {delegator} to {validator}")
else:
    logging.error("mismatch in delegation amount!!")

# redelegation tx
status, delegate_tx = tx_delegate("account1", dst_val_address, amount_to_be_sent)
assert status, f"delegation tx status:: {status}"
time.sleep(3)

# query redelegated amount
before_redel_amount = query_delegator_delegations(delegator, dst_val_address)[1][
    "balance"
]["amount"]

# redelegation tx
status, redelegate_tx = tx_redelegate(
    "account1", validator, dst_val_address, amount_to_be_sent
)
assert status, f"redelegation tx status :: {status}"
time.sleep(3)

# query redelegated amount and match the amount before and after the tx
after_redel_amount = query_delegator_delegations(delegator, dst_val_address)[1][
    "balance"
]["amount"]
if (int(before_redel_amount) + amount_to_be_sent) == int(after_redel_amount):
    logging.info(
        f"redelegation tx was successfull from {delegator} to {dst_val_address}"
    )
else:
    logging.error("tx failed! mismatch in redelegation amount.")


# unbond tx
status, unbond_tx = tx_unbond("account1", validator, amount_to_be_sent)
assert status, f"unbond tx status :: {status}"
time.sleep(3)

# query unbond tx and check the unbonded amount
status, unbond_amount = query_unbonding_delegation(delegator, validator)
unbond_balance = unbond_amount["entries"][0]["balance"]
if amount_to_be_sent == int(unbond_balance):
    logging.info(f"unbond tx is successfull!!!")
else:
    logging.error("error in unbond tx!!!")

# create validator
temp_dir = tempfile.TemporaryDirectory()
temp_dir_name = temp_dir.name
TEMP_VAL = "validator-10000"

command = f"{DAEMON} init testvalidator --home {temp_dir_name}"
tx, tx_err = exec_command(command)
assert len(tx_err), f"init tx res :: {tx}"

status, create_val_tx = tx_create_validator(
    "account1", amount_to_be_sent, TEMP_VAL, temp_dir_name
)
assert status, f"create-validator tx status :: {status}"
time.sleep(3)

(_, validator) = keys_show("account1", "val")

# query unbond tx and check the unbonded amount
status, validator_tx = query_validator(validator["address"])
if not status:
    logging.error(f"query validator status :: {status}")
else:
    val_name = validator_tx["description"]["moniker"]
    if val_name == TEMP_VAL:
        logging.info("validator created successfully!!!")
    else:
        logging.error(f"no validator found with name {TEMP_VAL}")


# clean tmp dir
temp_dir.cleanup()
