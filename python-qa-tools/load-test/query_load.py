import argparse, sys, logging
from core.keys import keys_show
from modules.bank.query import query_balances
from modules.staking.query import query_staking_delegations, query_staking_validators
from utils.types import account_type, num_txs_type

logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
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
    status, bTx = query_balances(sender)
    if not status:
        logging.error(bTx)
    else:
        bTxres = bTx["balances"][0]
        logging.info(f"Balance :: {bTxres}")

    # Fetch staking validators
    status, sTx = query_staking_validators()
    if not status:
        logging.error(sTx)    
    else:
        monikers = ""
        for validator in sTx['validators']:
            monikers += f"{validator['description']['moniker']} "
        logging.info(f"Monikers :: {monikers}")

    # Fetch staking delegations
    status, dTx = query_staking_delegations(sender, val1)
    if not status:
        logging.error(dTx)
    else:
        logging.info(f"Delegations :: {dTx['delegation']['shares']}")
