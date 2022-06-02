#/bin/sh

## This script verifies if all the necessary env variables are configured or exported for the setup scripts to
## work. If any of the values are not configured in env file or exported then a message is displayed which reminds the user
## to export them.

display_usage() {
    printf "** Please configure env file or export all the necessary env variables  :: **\n Daemon : $DAEMON\n Denom : $DENOM\n ChainID : $CHAINID\n DaemonHome : $DAEMON_HOME\n \n Github URL : $GH_URL\n Chain Version : $CHAIN_VERSION\n"
    exit 1
}

if [ -z $DAEMON ] || [ -z $DENOM ] || [ -z $CHAINID ] || [ -z $DAEMON_HOME ] || [ -z $GH_URL ] || [ -z $CHAIN_VERSION ] || [ -z $RPC ]
then 
    display_usage
fi
