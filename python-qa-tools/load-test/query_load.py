import argparse, os, sys
from core.keys import keys_show
from modules.bank.query import query_balances
from modules.staking.query import query_staking_delegations, query_staking_validators
from utils.types import account_type, num_txs_type

DAEMON = os.getenv('DAEMON')
DENOM = os.getenv('DENOM')
CHAINID = os.getenv('CHAINID')
DAEMON_HOME = os.getenv('DAEMON_HOME')
HOME = os.getenv('HOME')
RPC = os.getenv('RPC')

parser = argparse.ArgumentParser(description='This program takes inputs for intializing tx query load test.')
parser.add_argument('-s', '--sender', type= account_type, default = keys_show("validator1")[1]['address'], help= 'From which account the transaction should be intialized')
parser.add_argument('-n', '--num_txs', type = num_txs_type, default = 1000, help= 'Number of transactions to be made, Min. should be 1000')
args = parser.parse_args()

acc1, num_txs = args.sender, int(args.num_txs)

status, val1 = keys_show(acc1, "val")
if not status:
    sys.exit(val1)
val1 = val1['address']

for i in range(0, num_txs):
    # Fetch balance of acc1
    status, bTx = query_balances(acc1)
    if not status:
        print(bTx)
    else:
        bTxres = bTx["balances"][0]
        print(f"** Balance :: {bTxres} **")

    # Fetch staking validators
    status, sTx = query_staking_validators()
    if not status:
        print(sTx)    
    else:
        monikers = ""
        for validator in sTx['validators']:
            monikers += f"{validator['description']['moniker']} "
        print(f"** Monikers :: {monikers} **")

    # Fetch staking delegations
    status, dTx = query_staking_delegations(acc1, val1)
    if not status:
        print(dTx)
    else:
        print(f"** Delegations :: {dTx['delegation']['shares']} **")
