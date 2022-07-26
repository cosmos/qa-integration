
set -e
source ./env 

GOV_DEFAULT_PERIOD="60s"
DOWNTIME_JAIL_DURATION="60s"
UNBONDING_PERIOD="60s"
EVIDENCE_AGE="60000000000"
NUM_ACCOUNTS=2
IMAGE="qa$DAEMON$CHAIN_VERSION"

echo "Number of validators :: $NUM_VALS"
echo "Docker image :: $IMAGE"
# remove validator daemon home directories if they already exist
for (( a=1; a<=$NUM_VALS; a++ ))
do
    rm -rf $PWD/localnet/$IMAGE-$a
done

echo "INFO: Setting up validator home directories"
for (( a=1; a<=$NUM_VALS; a++ ))
do
    echo "INFO: Creating validator-$a home directory :: $PWD/localnet/$IMAGE-$a"
    mkdir -p $PWD/localnet/$IMAGE-$a/cosmovisor/genesis/bin
done

echo "INFO: Initializing the chain ($CHAINID)"
for (( a=1; a<=$NUM_VALS; a++ ))
do
    echo "INFO: Initializing validator-${a} configuration files"
    docker run -i -v $PWD/localnet/$IMAGE-$a:/node$a --rm $IMAGE sh -c "$DAEMON init --chain-id $CHAINID --home /node${a} moniker-${a}" > /dev/null 
done

echo "INFO: Creating $NUM_VALS keys"
for (( a=1; a<=$NUM_VALS; a++ ))
do
    docker run -i -v $PWD/localnet/$IMAGE-$a:/node$a --rm $IMAGE sh -c "$DAEMON keys add validator${a} --keyring-backend test --home /node${a}" > /dev/null 
done

# create accounts if second argument is passed
if [ -z $NUM_ACCOUNTS ] || [ "$NUM_ACCOUNTS" -eq 0 ]
then
    echo "INFO: Second argument was empty, not setting up additional account"
else
    echo "INFO: Creating $NUM_ACCOUNTS additional accounts"
    for (( a=1; a<=$NUM_ACCOUNTS; a++ ))
    do
        docker run -i -v $PWD/localnet/$IMAGE-1:/node1 --rm $IMAGE sh -c "$DAEMON keys add account${a} --keyring-backend test --home /node1" > /dev/null 
    done
fi

echo "INFO: Setting up genesis"
echo "INFO: Adding validator accounts to genesis"
for (( a=1; a<=$NUM_VALS; a++ ))
do
    if [ $a == 1 ]
    then
        docker run -i -v $PWD/localnet/$IMAGE-$a:/node$a --rm $IMAGE sh -c "$DAEMON add-genesis-account validator$a 1000000000000$DENOM --keyring-backend test --home /node${a}"
        echo "INFO: Done $PWD/localnet/$IMAGE-$a genesis creation "
        continue
    fi
    docker run -i -v $PWD/localnet/$IMAGE-$a:/node$a --rm $IMAGE sh -c "$DAEMON add-genesis-account validator${a} 1000000000000$DENOM --keyring-backend test --home /node${a}"
    chmod +x ./scripts/add_genesis.sh
    cp ./scripts/add_genesis.sh $PWD/localnet/$IMAGE-1/run.sh
    docker run -i -e VALADDR="validator$a" -e DENOM="$DENOM" -e DAEMON="$DAEMON" -v $PWD/localnet/$IMAGE-1:/node1 -v $PWD/localnet/$IMAGE-$a:/node2 --rm $IMAGE sh -c "/node1/run.sh"
done

echo "INFO: Adding additional accounts to genesis"
if [ -z $NUM_ACCOUNTS ]
then
    echo "INFO: Second argument was empty, not setting up additional account"
else
    for (( a=1; a<=$NUM_ACCOUNTS; a++ ))
    do
        docker run -i -v $PWD/localnet/$IMAGE-1:/node1 --rm $IMAGE sh -c "$DAEMON add-genesis-account account$a 1000000000000$DENOM --keyring-backend test --home /node1"
    done
fi


echo "INFO: Generating gentxs for validator accounts"
for (( a=1; a<=$NUM_VALS; a++ ))
do
    docker run -i -v $PWD/localnet/$IMAGE-$a:/node$a --rm $IMAGE sh -c "$DAEMON gentx validator$a 90000000000$DENOM --chain-id $CHAINID --keyring-backend test --home /node${a}"
done

echo "INFO: Copying all gentxs to $PWD/localnet/$IMAGE-1"
for (( a=2; a<=$NUM_VALS; a++ ))
do
    cp $PWD/localnet/$IMAGE-$a/config/gentx/*.json $PWD/localnet/$IMAGE-1/config/gentx/
done

echo "INFO: Collecting gentxs into $PWD/localnet/$IMAGE-1"
docker run -i -v $PWD/localnet/$IMAGE-1:/node1 --rm $IMAGE sh -c "$DAEMON collect-gentxs --home /node1"  > /dev/null 

DAEMON_HOME=$PWD/localnet/$IMAGE

echo "INFO: Updating genesis values"
sed -i "s/172800000000000/${EVIDENCE_AGE}/g" $DAEMON_HOME-1/config/genesis.json
sed -i "s/172800s/${GOV_DEFAULT_PERIOD}/g" $DAEMON_HOME-1/config/genesis.json
sed -i "s/stake/$DENOM/g" $DAEMON_HOME-1/config/genesis.json
sed -i 's/"downtime_jail_duration": "600s"/"downtime_jail_duration": "'${DOWNTIME_JAIL_DURATION}'"/' $DAEMON_HOME-1/config/genesis.json
sed -i 's/"unbonding_time": "1814400s"/"unbonding_time": "'${UNBONDING_PERIOD}'"/' $DAEMON_HOME-1/config/genesis.json

echo "INFO: Distribute genesis.json of $IMAGE-1 to remaining nodes"
for (( a=2; a<=$NUM_VALS; a++ ))
do
    cp -v $DAEMON_HOME-1/config/genesis.json $PWD/localnet/$IMAGE-$a/config/
done

# updating config.toml
for (( a=1; a<=$NUM_VALS; a++ ))
do
    DIFF=$(($a - 1))
    INC=$(($DIFF * 2))
    RPC=$((16657 + $INC)) #increment rpc ports
    LADDR=$((16656 + $INC)) #increment laddr ports
    GRPC=$((9092 + $INC)) #increment grpc poprt
    WGRPC=$((9093 + $INC)) #increment web grpc port
    echo "INFO: Updating validator-$a chain config"
    sed -i 's#tcp://127.0.0.1:26657#tcp://0.0.0.0:'${RPC}'#g' $DAEMON_HOME-$a/config/config.toml
    sed -i 's#tcp://0.0.0.0:26656#tcp://0.0.0.0:'${LADDR}'#g' $DAEMON_HOME-$a/config/config.toml
    sed -i '/allow_duplicate_ip =/c\allow_duplicate_ip = true' $DAEMON_HOME-$a/config/config.toml
    sed -i '/pprof_laddr =/c\# pprof_laddr = "localhost:6060"' $DAEMON_HOME-$a/config/config.toml
    sed -i 's#0.0.0.0:9090#0.0.0.0:'${GRPC}'#g' $DAEMON_HOME-$a/config/app.toml
    sed -i 's#0.0.0.0:9091#0.0.0.0:'${WGRPC}'#g' $DAEMON_HOME-$a/config/app.toml
    sed -i 's#enable = true#enable = false#g' $DAEMON_HOME-$a/config/app.toml
    sed -i '/max_num_inbound_peers =/c\max_num_inbound_peers = 140' $DAEMON_HOME-$a/config/config.toml
    sed -i '/max_num_outbound_peers =/c\max_num_outbound_peers = 110' $DAEMON_HOME-$a/config/config.toml
    sed -i '/skip_timeout_commit = false/c\skip_timeout_commit = true' $DAEMON_HOME-$a/config/config.toml
done

chmod +x ./scripts/update_peers.sh
cp ./scripts/update_peers.sh ./localnet
chmod +x ./localnet/update_peers.sh

docker run -i -e DAEMON="$DAEMON" -e NUM_VALS=$NUM_VALS -e IMAGE="$IMAGE" -v $PWD/localnet:/localnet --rm $IMAGE bash -c "/localnet/update_peers.sh"

## Creating the docker-compose with yq 
DEFAULT_DC_IP="192.168.10"
for (( a=1; a<=$NUM_VALS; a++ ))
do
    DIFF=$(($a - 1))
    INC=$(($DIFF * 2))
    RPC=$((16657 + $INC)) #increment rpc ports
    LADDR=$((16656 + $INC)) #increment laddr ports
    GRPC=$((9092 + $INC)) #increment grpc poprt
    WGRPC=$((9093 + $INC)) #increment web grpc port
    LCD=$((1317 + $INC)) #increment web grpc port
    ## Replace docker image 
    cp dc-template.yaml /tmp/$IMAGE-$a.yaml
    yq e -i ".services.node.container_name = \"${IMAGE}node${a}\"" /tmp/$IMAGE-$a.yaml
    yq e -i ".services.node.image = \"$IMAGE\"" /tmp/$IMAGE-$a.yaml
    IP_INCR=$(($a + 1))
    yq e -i ".services.node.networks.localnet.ipv4_address = \"$DEFAULT_DC_IP.$IP_INCR\"" /tmp/$IMAGE-$a.yaml
    yq e -i ".services.node.volumes[0] = \"./localnet/${IMAGE}-${a}:/app:Z\"" /tmp/$IMAGE-$a.yaml
    if [ $a == 1 ]
    then
        yq e -i ".services.node.volumes[1] = \"./internal:/internal:Z\"" /tmp/$IMAGE-$a.yaml
    fi
    ## PORTS 
    yq e -i ".services.node.ports[0] = \"${LADDR}:${LADDR}\"" /tmp/$IMAGE-$a.yaml
    yq e -i ".services.node.ports[1] = \"${LCD}:${LCD}\"" /tmp/$IMAGE-$a.yaml
    yq e -i ".services.node.ports[2] = \"${GRPC}:${GRPC}\"" /tmp/$IMAGE-$a.yaml
    yq e -i ".services.node.ports[3] = \"${WGRPC}:${WGRPC}\"" /tmp/$IMAGE-$a.yaml
    yq e -i ".services.node.ports[4] = \"${RPC}:${RPC}\"" /tmp/$IMAGE-$a.yaml

    yq "with(.services;with_entries(.key |= \"node${a}\"))" -i /tmp/$IMAGE-$a.yaml

done

## Creating the docker-compose.yaml
yq eval-all '... comments=""|. as $item ireduce ({}; . * $item)|sort_keys(..)' /tmp/$IMAGE-*.yaml > $IMAGE-docker-compose.yaml
yq eval-all '... comments=""|. as $item ireduce ({}; . * $item)|sort_keys(..)' mongo-dc-template.yaml $IMAGE-docker-compose.yaml > docker-compose.yaml

echo "docker-compose file creation is done
Use : $ docker-compose up 
It will spin the all nodes
-------------------------------------------------------------
JSON RPC : http://localhost:16657
API      : http://localhost:1317
-------------------------------------------------------------
"

rm -rf /tmp/$IMAGE-*.yaml