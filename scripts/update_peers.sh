for (( a=1; a<=$NUM_VALS; a++ ))
do
    echo "[INFO]>> Getting node-id of validator-$a"
    nodeID=$($DAEMON tendermint show-node-id --home /localnet/$IMAGE-$a)
    echo "nodeID $nodeID"
    PR="$nodeID@${IMAGE}node${a}:26656"
    echo "PR $PR"
    if [ $a == 1 ]
    then
        PERSISTENT_PEERS="${PR}"
        continue
    fi
    PERSISTENT_PEERS="${PERSISTENT_PEERS},${PR}"
done

for (( a=1; a<=$NUM_VALS; a++ ))
do
    sed -i '/persistent_peers =/c\persistent_peers = "'"$PERSISTENT_PEERS"'"' /localnet/$IMAGE-$a/config/config.toml
done