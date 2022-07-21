for (( a=1; a<=$NUM_VALS; a++ ))
do
    DIFF=$(($a - 1))
    INC=$(($DIFF * 2))
    LADDR=$((16656 + $INC))
    echo "INFO: Getting node-id of validator-$a"
    nodeID=$($DAEMON tendermint show-node-id --home /localnet/$IMAGE-$a)
    PR="$nodeID@node${a}:$LADDR"
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