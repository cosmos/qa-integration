import argparse, os, sys, time, logging
from core.keys import keys_show
from modules.auth.query import account_type, query_account

from modules.staking.tx import tx_delegate, tx_redelegate, tx_unbond
from modules.staking.query import query_all_redelegations, query_staking_delegations, query_staking_redelegation, query_unbonding_delegation

HOME = os.getenv('HOME')
logging.basicConfig(format='%(message)s',
                    level=logging.DEBUG)

validator = keys_show("validator1", "val", 1)[1]['address']
print(f"Keys...{validator}")

delegator = keys_show("account1", "acc", 1)[1]['address']
print(f"Keys...{delegator}")

parser = argparse.ArgumentParser(description='This program takes inputs for staking delegation load test.')
parser.add_argument('-s', '--sender', type = account_type, default = keys_show("account1", "acc", 1)[1]['address'], help = 'Account name')
#parser.add_argument('-r', '--receiver', type= account_type, default = keys_show("validator1", "val")[1]['address'], help= 'Receiver validator address')
#parser.add_argument('-n', '--num_txs', type = validate_num_txs, default = 1, help= 'Number of transactions to be made, should be positive integer')
args = parser.parse_args()
sender, amount_to_be_sent = args.sender, 5

if sender == validator:
    sys.exit('Error: The values of arguments "sender" and "receiver" are equal make sure to set different values')

print(f"opr addrrss...{validator}")

before_del_amount = query_staking_delegations(delegator, validator)[1]['balance']['amount']
print(f"before amount..{before_del_amount}")

status, delegateTx = tx_delegate("account1", validator, amount_to_be_sent, 00)
if not status:
    logging.error(f"{delegateTx}")
else:
    logging.info(f"TX HASH to :: {delegateTx['txhash']}")

logging.info('waiting for tx confirmation, avg time is 7s.')
time.sleep(7)

del_status, delegations = query_staking_delegations(delegator, validator)
if not del_status:
    logging.error(f"query staking delegations status :: {del_status}")
else:
    logging.info(f"Delegations......{delegations}")

# ******* query delegations **********

after_del_amount = query_staking_delegations(delegator, validator)[1]['balance']['amount']

if (int(before_del_amount )+ amount_to_be_sent) == int(after_del_amount):
    logging.info(f"delegation tx was successfull from {delegator} to {validator}")
else:
    logging.error("mismatch in delegation amount...")

print("check regelegation tx")

dst_val_address = keys_show("validator2", "val", 2)[1]['address']
print(f"Keys...{dst_val_address}")

status, redelegateTx = tx_redelegate("account1", validator, dst_val_address, amount_to_be_sent)
if not status:
    logging.error(f"redelegation tx status :: {status}")
else:
    logging.info(f"TX HASH to :: {redelegateTx['txhash']}")

logging.info('waiting for redelegate tx confirmation, avg time is 7s.')
time.sleep(7)

#print(f"tx hashhhhh...{redelegateTx['txhash']}")
# ************   query redelegations   **************

#redelegations = query_all_redelegations(delegator)
#print(f"redelegations.....{redelegations}")

#redelegate = query_staking_redelegation(delegator, validator, dst_val_address)
#print(f"val redelegation.......{redelegate}")


# *********** unbond tx ***************

status, unbond_tx = tx_unbond("account1",validator, amount_to_be_sent)
if not status:
    logging.error(f"unbond tx status :: {status}")
else:
    logging.info(f"unbond tx is successfull :: {unbond_tx}")

logging.info('waiting for unbond tx confirmation, avg time is 7s.')
time.sleep(7)

acc = query_unbonding_delegation(delegator, validator)
print(f"unbonddddd.....{acc}")