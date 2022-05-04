import argparse, os, sys
from modules.bank.query import query_balances
from utils.keys import fetch_account_address
from utils.staking import fetch_staking_delegations, fetch_staking_validators
from utils.types import validator_account_type

DAEMON = os.getenv('DAEMON')
DENOM = os.getenv('DENOM')
CHAINID = os.getenv('CHAINID')
DAEMON_HOME = os.getenv('DAEMON_HOME')
HOME = os.getenv('HOME')

parser = argparse.ArgumentParser(description='This program takes inputs for intializing tx query load test.')
parser.add_argument('ACC', type= validator_account_type, help= 'From which account the transaction should be intialized')
args = parser.parse_args()

ACC = int(args.ACC)

IP = "127.0.0.1"
PORT = "16657"
RPC = f"http://{IP}:{PORT}"

acc1, acc1err = fetch_account_address(f"validator{ACC}")
if len(acc1err):
    sys.exit(acc1err)

val1, val1err = fetch_account_address(f"validator{ACC}", "bech32")
if len(val1err):
    sys.exit(val1err)

for i in range(1, 10000):
    # Fetch balance of acc1
    bTx, bTxerr = query_balances(acc1, RPC)
    if len(bTxerr):
        print(bTxerr)
    else:
        bTxres = bTx["balances"][0]
        print(f"** Balance :: {bTxres} **")

    # Fetch staking validators
    sTx, sTxerr = fetch_staking_validators(RPC)
    if len(sTxerr):
        print(sTxerr)    
    else:
        monikers = ""
        for validator in sTx['validators']:
            monikers += f"{validator['description']['moniker']} "
        print(f"** Monikers :: {monikers} **")

    # Fetch staking delegations
    dTx, dTxerr = fetch_staking_delegations(acc1, val1, RPC)
    if len(dTxerr):
        print(dTxerr)
    else:
        dTxres = dTx['delegation']['shares']
        print(f"** Delegations :: {dTxres} **")
