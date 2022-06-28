#/bin/sh

## This script creates the necessary folders for cosmovisor. It also builds and places
## the binaries in the folders depending on the upgrade name.

set -e

# get absolute parent directory path of current file
CURPATH=`dirname $(realpath "$0")`
echo $CURPATH
cd $CURPATH

# check environment variables are set
. ../deps/env-check.sh

# NUM_VALS represents number of validator nodes
NUM_VALS=$1
if [ -z $NUM_VALS ]
then
    NUM_VALS=2
fi

echo "INFO: Building binary with upgraded version"
cd $HOME
export REPO=$(basename $GH_URL .git)
if [ ! -d $REPO ]
then
    git clone $GH_URL
fi
cd $REPO
git fetch --all && git checkout $UPGRADE_VERSION
make build
for (( a=1; a<=$NUM_VALS; a++ ))
do
    export DAEMON_HOME_$a=$DAEMON_HOME-$a
    mkdir -p "$DAEMON_HOME-$a"/cosmovisor/upgrades/$UPGRADE_NAME/bin
    cp ~/$REPO/build/$DAEMON "$DAEMON_HOME-$a"/cosmovisor/upgrades/$UPGRADE_NAME/bin/
done

CURRENT_BLOCK_HEIGHT=$($DAEMON status --node $RPC | jq '.SyncInfo.latest_block_height|tonumber')

echo "INFO: Submitting software upgrade proposal for upgrade: $UPGRADE_NAME"
$DAEMON tx gov submit-proposal software-upgrade $UPGRADE_NAME --title $UPGRADE_NAME \
    --description upgrade --upgrade-height $((CURRENT_BLOCK_HEIGHT + 60)) --deposit 10000000$DENOM \
    --from validator1 --yes --keyring-backend test --home $DAEMON_HOME-1 --node $RPC --chain-id $CHAINID

sleep 3s

echo "INFO: Voting on created proposal"
$DAEMON tx gov vote 1 yes --from validator1 --yes --keyring-backend test \
    --home $DAEMON_HOME-1 --node $RPC --chain-id $CHAINID

echo "INFO: Waiting for proposal to pass and upgrade"
sleep 60s

QUERY_COMMAND=`curl -s "$RPC/abci_query?path=%22/app/version%22" | jq -r '.result.response.value' | base64 -d && echo`
count=0

while [[ ($QUERY_COMMAND!=$UPGRADE_VERSION) && (count -le 5) ]]; do
    count=$((count+1))
    sleep 20s
done

if [[ $count -eq 6 ]]; then
    echo "ERROR: Upgrade failed with binary issues"
    exit 0
fi

# moving back to current file folder
cd $CURPATH

# testing all txs and queries
bash ./all_modules.sh
