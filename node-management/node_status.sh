#/bin/sh

## This script displays the latest block height and sync status of the nodes

NODES=$1
if [ -z $NODES ]
then
    NODES=1
fi

echo "**** Number of nodes for status checks: $NODES ****"
IP="$(dig +short myip.opendns.com @resolver1.opendns.com)"

if [ -z $IP ]
then
    IP=127.0.0.1
fi

echo "------- Query node status ---------"
for (( a=1; a<=$NODES; a++ ))
do
    DIFF=`expr $a - 1`
    INC=`expr $DIFF \* 2`
    PORT=`expr 16657 + $INC` 
    RPC="http://${IP}:${PORT}/status?"
    result=$(curl -s "${RPC}")
    height=$(echo "${result}" | jq -r '.result.sync_info.latest_block_height')
    syncStatus=$(echo "${result}" | jq -r '.result.sync_info.catching_up')
    echo "** rpc : $RPC , latest_block_height : $height , catching_up : $syncStatus **"
done
