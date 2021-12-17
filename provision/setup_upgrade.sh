#/bin/sh

display_usage() {
    printf "** Please check the exported values:: **\n Daemon : $DAEMON\n Denom : $DENOM\n ChainID : $CHAINID\n DaemonHome : $DAEMON_HOME\n \n Github URL : $GH_URL\n Chain Version : $CHAIN_VERSION\n Upgrade Name : $UPGRADE_Name\n Upgrade Version : $UPGRADE_VERSION\n"
    exit 1
}

if [ -z $DAEMON ] || [ -z $DENOM ] || [ -z $CHAINID ] || [ -z $DAEMON_HOME ] || [ -z $GH_URL ] || [ -z $CHAIN_VERSION ] || [ -z $UPGRADE_NAME ] || [ -z $UPGRADE_VERSION ]
then 
    display_usage
fi

# read no.of nodes to be upgraded
NODES=$1
if [ -z $NODES ]
then
    NODES=2
fi

cd $HOME
export REPO=$(basename $GH_URL .git)
rm -rf $REPO
git clone $GH_URL && cd $REPO
git fetch && git checkout $UPGRADE_VERSION
make build

for (( a=1; a<=$NODES; a++ ))
do
    export DAEMON_HOME_$a=$DAEMON_HOME-$a
    mkdir -p "$DAEMON_HOME-$a"/cosmovisor/upgrades/$UPGRADE_NAME/bin
	cp ~/$REPO/build/$DAEMON "$DAEMON_HOME-$a"/cosmovisor/upgrades/$UPGRADE_NAME/bin/
done


