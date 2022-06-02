#/bin/sh

## This script creates the necessary folders for cosmovisor. It also builds and places
## the binaries in the folders depending on the upgrade name.

set -e

# get absolute parent directory path of current file
CURPATH=`dirname $(realpath "$0")`
cd $CURPATH

# set environment with env config.
set -a
source ../env
set +a

# check environment variables are set
bash ../deps/env-check.sh $CURPATH

# NUM_VALS represents number of validator nodes
NUM_VALS=$1
if [ -z $NUM_VALS ]
then
    NUM_VALS=2
fi

cd $HOME
export REPO=$(basename $GH_URL .git)
rm -rf $REPO
git clone $GH_URL && cd $REPO
git fetch && git checkout $UPGRADE_VERSION
make build
for (( a=1; a<=$NUM_VALS; a++ ))
do
    export DAEMON_HOME_$a=$DAEMON_HOME-$a
    mkdir -p "$DAEMON_HOME-$a"/cosmovisor/upgrades/$UPGRADE_NAME/bin
    cp ~/$REPO/build/$DAEMON "$DAEMON_HOME-$a"/cosmovisor/upgrades/$UPGRADE_NAME/bin/
done
