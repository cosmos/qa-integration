#/bin/sh

## This script stops the systemd process of the nodes and removes their data directories.

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
    NUM_VALS=1
fi

echo "INFO: Number of validator nodes to be shutdown and disabled: $NUM_VALS"
echo "---------- Stopping systemd service files --------"
for (( a=1; a<=$NUM_VALS; a++ ))
do
    sudo -S systemctl stop $DAEMON-${a}.service
    echo "-- Stopped $DAEMON-${a}.service --"
done
echo "------- Running unsafe reset all ---------"
for (( a=1; a<=$NUM_VALS; a++ ))
do
    $DAEMON tendermint unsafe-reset-all  --home $DAEMON_HOME-$a    
    rm -rf $DAEMON_HOME-$a
    echo "-- Executed $DAEMON unsafe-reset-all  --home $DAEMON_HOME-$a --"
done
echo "---------- Disabling systemd process files --------"
for (( a=1; a<=$NUM_VALS; a++ ))
do
   sudo -S systemctl disable $DAEMON-${a}.service
   echo "-- Executed sudo -S systemctl disable $DAEMON-${a}.service --"
done
