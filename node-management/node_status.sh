#/bin/sh

## This script displays the latest block height and sync status of the nodes

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

echo "INFO: Number of validator nodes for status checks:  : $NUM_VALS"
IP="$(dig +short myip.opendns.com @resolver1.opendns.com)"

if [ -z $IP ]
then
    IP=127.0.0.1
fi

echo "------- Query node status ---------"
for (( a=1; a<=$NUM_VALS; a++ ))
do
    DIFF=`expr $a - 1`
    INC=`expr $DIFF \* 2`
    PORT=`expr 16657 + $INC` 
    RPC="http://${IP}:${PORT}/status?"
    result=$(curl -s "${RPC}")
    height=$(echo "${result}" | jq -r '.result.sync_info.latest_block_height')
    syncStatus=$(echo "${result}" | jq -r '.result.sync_info.catching_up')
    echo "STATUS of validator-$a: rpc : $RPC , latest_block_height : $height , catching_up : $syncStatus **"
done
