#/bin/sh

## This script pauses the systemd process of the nodes.

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

echo "INFO: Number of validator nodes to be paused: $NUM_VALS"
echo "---------- Stopping systemd service files --------"
for (( a=1; a<=$NUM_VALS; a++ ))
do
    sudo -S systemctl stop $DAEMON-${a}.service
    echo "-- Stopped $DAEMON-${a}.service --"
done
