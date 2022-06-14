#/bin/sh

# This script verifies if all the necessary env variables are configured or exported for the setup scripts to
# work. If any of the values are not configured in env file or exported then a message is displayed which reminds the user
# to export them.

# set environment with env config.
set -a
source ../env
set +a

# set pythonpath environment with absolute path of python-qa-tools directory
cd ..
export PYTHONPATH=$PWD:$PWD/python-qa-tools
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
