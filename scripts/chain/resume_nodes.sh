#/bin/sh

## This script restarts the systemd process of the nodes. 

set -e

# get absolute parent directory path of current file
CURPATH=`dirname $(realpath "$0")`
cd $CURPATH

# check environment variables are set
. ../deps/env-check.sh

# NUM_VALS represents number of validator nodes
NUM_VALS=$1
if [ -z $NUM_VALS ]
then
    NUM_VALS=1
fi

echo "INFO: Number of validator nodes to be resumed: $NUM_VALS"
echo "---------- Restarting systemd service files --------"
for (( a=1; a<=$NUM_VALS; a++ ))
do
    sudo -S systemctl restart $DAEMON-${a}.service
    echo "-- Resumed $DAEMON-${a}.service --"
done
