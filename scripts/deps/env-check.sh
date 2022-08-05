#/bin/sh

# This script verifies if all the necessary env variables are configured or exported for the setup scripts to
# work. If any of the values are not configured in env file or exported then a message is displayed which reminds the user
# to export them.

# set environment with env config.
set -a
source ../../env-umee
set +a

# set pythonpath environment with absolute path of internal directory
cd ../..
export PYTHONPATH=$PWD:$PWD/internal
export GOROOT=/usr/local/go
export GOPATH=$HOME/go
export GOBIN=$GOPATH/bin
export PATH=$PATH:/usr/local/go/bin:$GOBIN

display_usage() {
    printf "** Please configure env file or export all the necessary env variables  :: **\n Daemon : $DAEMON\n Denom : $DENOM\n ChainID : $CHAINID\n DaemonHome : $DAEMON_HOME\n \n Github URL : $GH_URL\n Chain Version : $CHAIN_VERSION\n"
    exit 1
}

if [ -z $DAEMON ] || [ -z $DENOM ] || [ -z $CHAINID ] || [ -z $DAEMON_HOME ] || [ -z $GH_URL ] || [ -z $CHAIN_VERSION ] || [ -z $RPC ] || [ -z $MONGO_URL ]
then
    display_usage
fi

if [ -z $NUM_VALS ]
then
    NUM_VALS = 3
fi

# export daemon home paths
for (( a=1; a<=$NUM_VALS; a++ ))
do
    export "NODE${a}_HOME"=$DAEMON_HOME-$a
done

# set NUM_TXS env if not found
if [[ -z $NUM_TXS || $(( $NUM_TXS )) -le 0 ]]
then
    export NUM_TXS=50
fi
