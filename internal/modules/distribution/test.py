from distutils.log import info
import json
import os,logging,time,subprocess
from core.keys import keys_show
from internal.utils import exec_command

from modules.distribution.tx import (
    tx_delegate,
    tx_fund_communitypool,
    tx_withdraw_addr,
    tx_withdraw_allrewards,
    tx_withdraw_commision_rewards,
    tx_withdraw_rewards
)
from modules.distribution.query import (
    query_balance,
    query_commission_rewards,
    query_community_pool,
    query_delegation,
    query_delegations,
    query_params,
    query_rewards,
    query_rewards_singleval,
    query_slashes,
    query_validator_outstanding_rewards
)

DAEMON_HOME = os.getenv("DAEMON_HOME")
HOME = os.getenv("HOME")
os.environ["node1_home"] = f"{DAEMON_HOME}-1"
os.environ["node2_home"] = f"{DAEMON_HOME}-2"
os.environ["node3_home"] = f"{DAEMON_HOME}-3"
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

cmd = f"sudo -S systemctl stop simd-3"
tx,tx_err = exec_command(cmd)
if len(tx_err):
    logging.error(tx_err)
# process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
# process.communicate()
time.sleep(3)

node2_home = os.getenv("node2_home")
node3_home = os.getenv("node3_home")

validator1 = keys_show("validator1","val")[1]["address"]
validator2 = keys_show("validator2","val",node2_home)[1]["address"]
validator3 = keys_show("validator3","val",node3_home)[1]["address"]
delegator1 = keys_show("account1","acc")[1]["address"]
delegator2 = keys_show("account2","acc")[1]["address"]

amount_to_be_sent = 100

#query delegations
status,delegations = query_delegation(delegator1,validator1)
if not status:
    # delegate tx
    status,delegate_tx = tx_delegate("account1",validator1,amount_to_be_sent)
    if not status:
        logging.error(f"error in delegate tx :: {delegate_tx}")
    else:
        logging.info(f"delegate tx :: {delegate_tx['txhash']}")

time.sleep(5)

# query delegations
status,delegations = query_delegation(delegator1,validator2)
if not status:
    # delegate tx 
    status,delegate_tx = tx_delegate("account1",validator2,amount_to_be_sent)
    if not status:
        logging.error(f"error in delegate tx :: {delegate_tx}")
    else:
        logging.info(f"delegate tx :: {delegate_tx['txhash']}")

time.sleep(10)

# query balance
before_balance = query_balance(delegator1)[1]["balances"][0]["amount"]
# query rewards
rewards = query_rewards_singleval(delegator1,validator1)[1]["rewards"][0]["amount"]
# withdraw rewards tx
status,rewards_tx = tx_withdraw_rewards("account1",validator1)
if not status:
    logging.error(f"error in tx withdraw rewards :: {rewards_tx}")
else:
    logging.info(f"tx_hash  :: {rewards_tx['txhash']}")
time.sleep(3)
after_balance = query_balance(delegator1)[1]["balances"][0]["amount"]
if int(after_balance) == (int(before_balance) + int(float(rewards))):
    logging.info(f"with-draw rewards tx of {delegator1} from {validator1} was successful")
else:
    logging.error("missmatch in rewards")

time.sleep(10)

# query delegations 
delegations = query_delegations(delegator1)[1]["delegation_responses"]
# query balance
before_balance = query_balance(delegator1)[1]["balances"][0]["amount"]
# query all rewards
all_rewards = query_rewards(delegator1)[1]["rewards"]
total = 0
for x in all_rewards:
    rewards = x["reward"][0]["amount"]
    total = total + (float(rewards))
# tx withdraw all rewards
status,all_rewards = tx_withdraw_allrewards("account1")
if not status:
    logging.error(f"error in tx withdraw all rewards :: {all_rewards}")
else:
    logging.info(f"all_rewards tx_hash  :: {all_rewards['txhash']}")
after_balance = query_balance(delegator1)[1]["balances"][0]["amount"]
if int(after_balance) == int(before_balance) + int(total):
    logging.info(f"withdraw all rewards of {delegator1} was successful")
else:
    logging.error(f"missmatch in rewards")

time.sleep(5)

# query balance
before_balance = query_balance(delegator1)[1]["balances"][0]["amount"]
# query community pool balance
community_pool = query_community_pool()[1]["pool"][0]["amount"]
# fund community pool tx 
status,fund_pool = tx_fund_communitypool("account1",amount_to_be_sent)
if not status:
    logging.error(f"error in tx fund community pool :: {fund_pool}")
else:
    logging.info(f"tx_hash :: {fund_pool['txhash']}")
after_balance = query_balance(delegator1)[1]["balances"][0]["amount"]
total = int(float(before_balance)) - int(amount_to_be_sent)
if int(after_balance) == int(before_balance) - int(amount_to_be_sent):
    logging.info("fund community pool tx was successful")
else:
    logging.error("missmatch in fund community pool")

time.sleep(5)

# tx set withdraw address
status,set_addr = tx_withdraw_addr("account1",delegator2)
if not status:
    logging.error(f"Error while set withdraw address :: {set_addr}")
else:
    logging.info(f"Set withdraw address tx hash:: {set_addr['txhash']}")
# query balance
before_balance = query_balance(delegator2)[1]["balances"][0]["amount"]
# query rewards
before_reward = query_rewards_singleval(delegator1,validator1)[1]["rewards"][0]["amount"]
# tx withdraw rewards
status,rewards = tx_withdraw_rewards("account2",validator1)
if not status:
    logging.error(f"Error in withdraw rewards :: {rewards}")
else:
    logging.info(f"withdraw rewards tx: {rewards['txhash']}")
# query balance
after_balance = query_balance(delegator2)[1]["balances"][0]["amount"]
if int(after_balance) == int(before_balance) + int(float(before_reward)):
    logging.info("Set withdraw rewards tx successfull")
else:
    logging.info("Set withdraw rewards tx failed")

time.sleep(3)

# query params
path = f"{HOME}/.simd-1/config/"
with open(path+'genesis.json') as file:
    data = json.load(file)
query_params = query_params()[1]
if data["app_state"]["distribution"]["params"] == query_params:
    logging.info("querying params was successful")
else:
    logging.error("missmatch in params")

time.sleep(5)

# query validator commission
commission = query_commission_rewards(validator1)[1]["commission"][0]["amount"]
# withdraw commission rewards
status,commission_rewards = tx_withdraw_commision_rewards("validator1",validator1)
if not status:
    logging.error(f"error in tx withdraw commission rewards :: {commission_rewards}")
else:
    logging.info(f"commission tx_hash :: {commission_rewards['txhash']}")
time.sleep(3)
rewards =  query_commission_rewards(validator1)[1]["commission"][0]["amount"]
status,commission_rewards = tx_withdraw_commision_rewards("validator1",validator1)
if not status:
    logging.error(f"error in tx withdraw commission rewards :: {commission_rewards}")
else:
    logging.info(f"commission tx_hash :: {commission_rewards['txhash']}")
time.sleep(2)
after_rewards =  query_commission_rewards(validator1)[1]["commission"][0]["amount"]
if int(float(after_rewards)) < int(float(rewards)) :
        logging.info("Commission rewards tx was successful")
else:
    logging.error("missmatch in validator commission rewards")

time.sleep(3)

# query validator slashes
slash_count = query_slashes(validator3,1,1000)[1]["slashes"]
if slash_count:
    logging.info(f"Querying slashes of {validator3} was successful")
else:
    logging.info("missmatch in slashes")

# Query validator outstanding rewards
outstanding_rewards = query_validator_outstanding_rewards(validator1)[1]["rewards"][0]["amount"]
if len(outstanding_rewards):
    logging.info(f"Querying {validator1} outstanding rewards was successful")
else:
    logging.info("missmatch in validator outstanding rewards")

