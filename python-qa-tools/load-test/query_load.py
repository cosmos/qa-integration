import argparse, sys, logging
from core.keys import keys_show
from modules.auth.query import account_type
from modules.bank.query import query_balances
from modules.staking.query import query_staking_delegations, query_staking_validators
from utils import num_txs_type

logging.basicConfig(format='%(message)s',
                    level=logging.DEBUG)

parser = argparse.ArgumentParser(description='This program takes inputs for intializing tx query load test.')
parser.add_argument('-s', '--sender', type= account_type, default = keys_show("validator1")[1]['address'], help= 'From which account the transaction should be intialized')
parser.add_argument('-n', '--num_txs', type = num_txs_type, default = 1000, help= 'Number of transactions to be made, atleast should be 1000')
args = parser.parse_args()

sender, num_txs = args.sender, int(args.num_txs)

status, val1 = keys_show(sender, "val")
if not status:
    sys.exit(val1)
val1 = val1['address']

for i in range(0, num_txs):
    # Fetch balance of sender
    status, balance_query_response = query_balances(sender)
    if not status:
        logging.error(balance_query_response)
    else:
        balance = balance_query_response["balances"][0]
        logging.info(f"Balance :: {balance}")

    # Fetch staking validators
    status, validators_response = query_staking_validators()
    if not status:
        logging.error(validators_response)    
    else:
        monikers = ""
        for validator in validators_response['validators']:
            monikers += f"{validator['description']['moniker']} "
        logging.info(f"Monikers :: {monikers}")

    # Fetch staking delegations
    status, delegations_response = query_staking_delegations(sender, val1)
    if not status:
        logging.error(delegations_response)
    else:
        logging.info(f"Delegations :: {delegations_response['delegation']['shares']}")
