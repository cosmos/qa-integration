#/bin/sh

# read no.of nodes to be upgraded
NODES=$1
if [ -z $NODES ]
then
    NODES=2
fi

RPC="http://127.0.0.1:16657"
cd $HOME
export REPO=$(basename $GH_URL .git)
rm -rf $REPO
git clone $GH_URL && cd $REPO
git fetch && git checkout $UPGRADE_VERSION
make build
currentHt=$("${DAEMON}" status --node http://localhost:16657 | jq .SyncInfo.latest_block_height)
upgradeHt=$(expr $currentHt + 1000)
propTx=$("${DAEMON}" tx gov submit-proposal software-upgrade "$UPGRADE_NAME" --upgrade-height "$upgradeHt" --from validator1 --deposit "10000$DENOM" --description "Upgrade test"  --keyring-backend test --home $DAEMON_HOME-1 --node $RPC --output json)
propTxhash=$(echo "${propTx}" | jq -r '.txhash')
sleep 7
queryProp=$("${DAEMON}" q tx $propTxhash --node $RPC --output json)
propId=$(echo "$queryProp" | jq .logs[0].events[4].attributes[0].value)
for (( a=1; a<=$NODES; a++ ))
do
    export DAEMON_HOME_$a=$DAEMON_HOME-$a
    mkdir -p "$DAEMON_HOME-$a"/cosmovisor/upgrades/$UPGRADE_NAME/bin
	cp ~/$REPO/build/$DAEMON "$DAEMON_HOME-$a"/cosmovisor/upgrades/$UPGRADE_NAME/bin/
    propVote=$("${DAEMON}" tx gov vote $propId yes --from validator$a --keyring-backend test --home $DAEMON_HOME-1 --node $RPC --output json -y)
    propVotehash=$(echo "${propVote}" | jq -r '.txhash')
    echo $propVotehash
done
