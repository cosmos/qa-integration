import argparse, os, sys, time, logging
from core.keys import keys_show
from modules.auth.query import account_type, query_account

from modules.staking.tx import tx_delegate
from modules.staking.query import query_staking_delegations

# tx_delegate()

HOME = os.getenv('HOME')
logging.basicConfig(format='%(message)s',
                    level=logging.DEBUG)

validator = keys_show("validator1", "val")[1]['address']
print(f"Keys...{validator}")

delegator = keys_show("account1", "acc")[1]['address']
print(f"Keys...{delegator}")

parser = argparse.ArgumentParser(description='This program takes inputs for staking delegation load test.')
parser.add_argument('-s', '--sender', type = account_type, default = keys_show("account1", "acc")[1]['address'], help = 'Account name')
#parser.add_argument('-r', '--receiver', type= account_type, default = keys_show("validator1", "val")[1]['address'], help= 'Receiver validator address')
#parser.add_argument('-n', '--num_txs', type = validate_num_txs, default = 1, help= 'Number of transactions to be made, should be positive integer')
args = parser.parse_args()
sender, amount_to_be_sent = args.sender, 10

if sender == validator:
    sys.exit('Error: The values of arguments "sender" and "receiver" are equal make sure to set different values')

print(f"opr addrrss...{validator}")

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