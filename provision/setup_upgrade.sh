#/bin/sh

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
