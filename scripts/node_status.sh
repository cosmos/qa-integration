#/bin/sh

NODES=$1
if [ -z $NODES ]
then
    NODES=1
fi

echo "**** Number of nodes to be check for the status: $NODES ****"

IP="$(dig +short myip.opendns.com @resolver1.opendns.com)"
echo "Public IP address: ${IP}"

if [ -z $IP ]
then
    IP=127.0.0.1
fi

echo "------- Query node status ---------"

for (( a=1; a<=$NODES; a++ ))
do
    DIFF=`expr $a - 1`
    INC=`expr $DIFF \* 2`
    PORT=`expr 16657 + $INC` #get ports

    RPC="http://${IP}:${PORT}/status?"
    result=$(curl -s "${RPC}")
    height=$(echo "${result}" | jq -r '.result.sync_info.latest_block_height')
    syncStatus=$(echo "${result}" | jq -r '.result.sync_info.catching_up')
    echo "** rpc : $RPC , latest_block_height : $height , catching_up : $syncStatus **"
done