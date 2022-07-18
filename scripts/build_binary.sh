#/bin/sh

source ./env 

REPO=$DAEMON-$CHAIN_VERSION

echo "[INFO]>> Clone the repo $GH_URL into $REPO"
if [ ! -d $REPO ]
then
    git clone -b $CHAIN_VERSION --single-branch $GH_URL $REPO
fi

## Docker image build the 
echo "FROM golang:1.18-alpine AS build-env

# Install minimum necessary dependencies
ENV PACKAGES curl make git libc-dev bash gcc linux-headers eudev-dev python3
RUN apk add --no-cache \$PACKAGES\

# Set working directory for the build
WORKDIR /project

# Add source files
COPY . .

# install simapp, remove packages
RUN make build

# Final image
FROM alpine:edge

# Install ca-certificates
RUN apk add --update ca-certificates
WORKDIR /root

EXPOSE 26656 26657 1317 9090
COPY --from=build-env /project/build/$DAEMON /usr/bin/$DAEMON
cmd [\"$DAEMON\",\"start\",\"--home\",\"/app\"]" > Dockerfile

echo "[INFO]>> Build the docker images with ${DAEMON} and version ${CHAIN_VERSION}"

IMAGE=qa$DAEMON$CHAIN_VERSION
if test ! -z "$(docker images -q $IMAGE:latest)"
then 
    echo "[INFO]>> $IMAGE is already exists"
else
    docker build -t $IMAGE -f ./Dockerfile ./$REPO
fi



echo "Installed $DAEMON version details:"
# check version
docker run -it --rm $IMAGE $DAEMON version 

NUM_VALS=4

echo "NUM_VALS $NUM_VALS"
# remove validator daemon home directories if they already exist
for (( a=1; a<=$NUM_VALS; a++ ))
do
    echo "DIR "$PWD/localnet/$IMAGE-$a
    rm -rf $PWD/localnet/$IMAGE-$a
done

echo "INFO: Setting up validator home directories"
for (( a=1; a<=$NUM_VALS; a++ ))
do
    echo "INFO: Creating validator-$a home directory :: $NODE_HOME-$a"
    mkdir -p $PWD/localnet/$IMAGE-$a/cosmovisor/genesis/bin
    # cp $(which $DAEMON) "$NODE_HOME-$a"/cosmovisor/genesis/bin/
done

echo "INFO: Initializing the chain ($CHAINID)"
for (( a=1; a<=$NUM_VALS; a++ ))
do
    echo "INFO: Initializing validator-${a} configuration files"
    # $DAEMON init --chain-id $CHAINID  --home /$NODE_HOME-${a}
    docker run -it -v $PWD/localnet/$IMAGE-$a:/node$a --rm $IMAGE sh -c "$DAEMON init --chain-id $CHAINID --home /node${a} moniker-${a}"
done

echo "---------Creating $NUM_VALS keys-------------"
for (( a=1; a<=$NUM_VALS; a++ ))
do
    docker run -it -v $PWD/localnet/$IMAGE-$a:/node$a --rm $IMAGE sh -c "$DAEMON keys add validator${a} --keyring-backend test --home /node${a}"
done


echo "[INFO]>> Setting up genesis"
echo "[INFO]>> Adding validator accounts to genesis"
for (( a=1; a<=$NUM_VALS; a++ ))
do
    if [ $a == 1 ]
    then
        docker run -it -v $PWD/localnet/$IMAGE-$a:/node$a --rm $IMAGE sh -c "$DAEMON add-genesis-account validator$a 1000000000000$DENOM --keyring-backend test --home /node${a}"
        echo "INFO: Done $PWD/localnet/$IMAGE-$a genesis creation "
        continue
    fi
    docker run -it -v $PWD/localnet/$IMAGE-$a:/node$a --rm $IMAGE sh -c "$DAEMON add-genesis-account validator${a} 1000000000000$DENOM --keyring-backend test --home /node${a}"
    VALADDR=$(docker run -it -v $PWD/localnet/$IMAGE-$a:/node$a --rm $IMAGE sh -c "$DAEMON keys show validator$a -a --keyring-backend test --home /node${a}")
    # echo "docker run -it -v $PWD/localnet/$IMAGE-1:/node1 --rm $IMAGE sh -c \"$DAEMON add-genesis-account $(echo -n $VALADDR) 1000000000000$DENOM --keyring-backend test --home /node1\""
    # docker run -it -e VALADDR="$VALADDR" -v $PWD/localnet/$IMAGE-1:/node1 --rm $IMAGE sh -c "$DAEMON add-genesis-account $VALADDR 1000000000000$DENOM --keyring-backend test --home /node1"
    # docker run -it -e VALADDR="$VALADDR" -e DENOM="$DENOM" -e DAEMON="$DAEMON" -v $PWD/localnet/$IMAGE-1:/node1 --rm $IMAGE sh -c "$DAEMON add-genesis-account \"$VALADDR\" \"1000000000000$DENOM\" --keyring-backend test --home /node1"
    VALADDR=`echo -n ${VALADDR}`
    echo $DAEMON
    echo $VALADDR
    echo $DENOM
    echo "$DAEMON add-genesis-account $VALADDR 1000000000000$DENOM --keyring-backend test --home /node1"
    # docker run -it -e VALADDR="$VALADDR" -e DENOM="$DENOM" -e DAEMON="$DAEMON" -v $PWD/localnet/$IMAGE-1:/node1 --rm $IMAGE sh -c "$CMD"
done


echo "[INFO]>> Generating gentxs for validator accounts"
for (( a=1; a<=$NUM_VALS; a++ ))
do
    docker run -it -v $PWD/localnet/$IMAGE-$a:/node$a --rm $IMAGE sh -c "$DAEMON gentx validator$a 90000000000$DENOM --chain-id $CHAINID --keyring-backend test --home /node${a}"
done

echo "[INFO]>> Copying all gentxs to $PWD/localnet/$IMAGE-1"
for (( a=2; a<=$NUM_VALS; a++ ))
do
    cp $PWD/localnet/$IMAGE-$a/config/gentx/*.json $PWD/localnet/$IMAGE-1/config/gentx/
done

echo "[INFO]>> Collecting gentxs into $PWD/localnet/$IMAGE-1"
docker run -it -v $PWD/localnet/$IMAGE-1:/node1 --rm $IMAGE sh -c "$DAEMON collect-gentxs --home /node1"

echo "[INFO]>> Distribute genesis.json of $IMAGE-1 to remaining nodes"
for (( a=2; a<=$NUM_VALS; a++ ))
do
    cp -v $PWD/localnet/$IMAGE-1/config/genesis.json $PWD/localnet/$IMAGE-$a/config/
done

for (( a=1; a<=$NUM_VALS; a++ ))
do
    echo "[INFO]>> Getting node-id of validator-$a"
    nodeID=$(docker run -it -v $PWD/localnet/$IMAGE-$a:/node$a --rm $IMAGE sh -c "${DAEMON} tendermint show-node-id --home /node${a}")
    ID=`echo -n $nodeID`
    # nodeID=$("${DAEMON}" tendermint show-node-id --home $DAEMON_HOME-$a)
    PR="$nodeID@${IMAGE}node${a}:26656"
    echo "--------------"
    echo "PR $PR"
    # PR=${PR//$'\n'/}
    if [ $a == 1 ]
    then
        PERSISTENT_PEERS="${PR}"
        continue
    fi
    PERSISTENT_PEERS=$(echo -n "${PERSISTENT_PEERS},${PR}")
done

PEERS=`echo -n ${PERSISTENT_PEERS//$'\n'/}`
echo "PERSISTENT_PEERS ${PEERS}"
# updating config.toml
echo "[INFO]>> Updating the PEER IDS"
DAEMON_HOME=$PWD/localnet/$IMAGE
for (( a=1; a<=$NUM_VALS; a++ ))
do
    echo "INFO: Updating validator-$a chain config"
    sed -i 's#tcp://127.0.0.1:26657#tcp://0.0.0.0:26657#g' $DAEMON_HOME-$a/config/config.toml
    sed -i 's#tcp://0.0.0.0:26656#tcp://0.0.0.0:26656#g' $DAEMON_HOME-$a/config/config.toml
    sed -i '/persistent_peers =/c\persistent_peers = "'"${PERSISTENT_PEERS//$\'\n\'/}"'"' $DAEMON_HOME-$a/config/config.toml
    sed -i '/allow_duplicate_ip =/c\allow_duplicate_ip = true' $DAEMON_HOME-$a/config/config.toml
    sed -i '/pprof_laddr =/c\# pprof_laddr = "localhost:6060"' $DAEMON_HOME-$a/config/config.toml
done



## Creating the docker-compose with yq 
DEFAULT_DC_IP="192.168.10"
RPCPORT=26656
GRPCPORT=26657
LCDPORT=1317
PPROF=6060
for (( a=1; a<=$NUM_VALS; a++ ))
do
    ## Replace docker image 
    cp dc-template.yaml /tmp/$IMAGE-$a.yaml
    yq e -i ".services.node.container_name = \"${IMAGE}node${a}\"" /tmp/$IMAGE-$a.yaml
    yq e -i ".services.node.image = \"$IMAGE\"" /tmp/$IMAGE-$a.yaml
    IP_INCR=$(($a + 1))
    yq e -i ".services.node.networks.localnet.ipv4_address = \"$DEFAULT_DC_IP.$IP_INCR\"" /tmp/$IMAGE-$a.yaml
    yq e -i ".services.node.volumes[0] = \"./localnet/${IMAGE}-${a}:/app:Z\"" /tmp/$IMAGE-$a.yaml
    ## PORTS 

    yq e -i ".services.node.ports[0] = \"${RPCPORT}-${GRPCPORT}:26656-26657\"" /tmp/$IMAGE-$a.yaml
    yq e -i ".services.node.ports[1] = \"${LCDPORT}:1317\"" /tmp/$IMAGE-$a.yaml
    yq e -i ".services.node.ports[2] = \"${PPROF}:9090\"" /tmp/$IMAGE-$a.yaml

    yq "with(.services;with_entries(.key |= \"${IMAGE}node${a}\"))" -i /tmp/$IMAGE-$a.yaml
   
   
    RPCPORT=$(($RPCPORT + 2))
    GRPCPORT=$(($GRPCPORT + 2))
    LCDPORT=$(($LCDPORT + 2))
    PPROF=$(($PPROF + 2))

done

## Creating the docker-compose with yq 
yq eval-all '... comments=""|. as $item ireduce ({}; . * $item)|sort_keys(..)' /tmp/$IMAGE-*.yaml > $IMAGE-docker-compose.yml
