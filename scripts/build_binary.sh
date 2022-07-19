#/bin/sh

GOV_DEFAULT_PERIOD="60s"
DOWNTIME_JAIL_DURATION="60s"
UNBONDING_PERIOD="60s"
EVIDENCE_AGE="60000000000"

set -e
source ./env 

REPO=$DAEMON-$CHAIN_VERSION

echo "[INFO]>> Clone the repo $GH_URL into $REPO"
if [ ! -d $REPO ]
then
    git clone -b $CHAIN_VERSION --single-branch $GH_URL $REPO
fi

## Docker 
echo "FROM golang:1.18-alpine AS build-env

# Install minimum necessary dependencies
ENV PACKAGES curl make git libc-dev bash gcc linux-headers eudev-dev python3
RUN apk add --no-cache \$PACKAGES\

RUN go install github.com/cosmos/cosmos-sdk/cosmovisor/cmd/cosmovisor@v1.0.0

# Set working directory for the build
WORKDIR /project

# Add source files
COPY . .

# install simapp, remove packages
RUN make build

# Final image
FROM alpine:edge

# Install deps 
RUN apk add --update ca-certificates python3 jq bash pylint python3-pip
WORKDIR /root

EXPOSE 26656 26657 1317 9090

COPY --from=build-env /project/build/$DAEMON /usr/bin/$DAEMON
COPY --from=build-env /go/bin/cosmovisor /usr/bin/cosmovisor

cmd [\"$DAEMON\",\"start\",\"--home\",\"/app\"]" > ${DAEMON}_Dockerfile

echo "[INFO]>> Build the docker images with ${DAEMON}_Dockerfile and version ${CHAIN_VERSION}"

IMAGE=qa$DAEMON$CHAIN_VERSION
if test ! -z "$(docker images -q $IMAGE:latest)"
then 
    echo "[INFO]>> docker image $IMAGE is already exists"
else
    docker build -t $IMAGE -f ./${DAEMON}_Dockerfile./$REPO
fi

# check version
echo "$DAEMON installed version $(docker run -it --rm $IMAGE $DAEMON version)"

NUM_VALS=4

echo "Number of validators :: $NUM_VALS"
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
    docker run -it -v $PWD/localnet/$IMAGE-$a:/node$a --rm $IMAGE sh -c "$DAEMON init --chain-id $CHAINID --home /node${a} moniker-${a}" > /dev/null 
done

echo "INFO: Creating $NUM_VALS keys"
for (( a=1; a<=$NUM_VALS; a++ ))
do
    docker run -it -v $PWD/localnet/$IMAGE-$a:/node$a --rm $IMAGE sh -c "$DAEMON keys add validator${a} --keyring-backend test --home /node${a}" > /dev/null 
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
    chmod +x ./scripts/add_genesis.sh
    cp ./scripts/add_genesis.sh $PWD/localnet/$IMAGE-1/run.sh
    docker run -it -e VALADDR="validator$a" -e DENOM="$DENOM" -e DAEMON="$DAEMON" -v $PWD/localnet/$IMAGE-1:/node1 -v $PWD/localnet/$IMAGE-$a:/node2 --rm $IMAGE sh -c "/node1/run.sh"
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

DAEMON_HOME=$PWD/localnet/$IMAGE

echo "[INFO]>> Updating genesis values"
sed -i "s/172800000000000/${EVIDENCE_AGE}/g" $DAEMON_HOME-1/config/genesis.json
sed -i "s/172800s/${GOV_DEFAULT_PERIOD}/g" $DAEMON_HOME-1/config/genesis.json
sed -i "s/stake/$DENOM/g" $DAEMON_HOME-1/config/genesis.json
sed -i 's/"downtime_jail_duration": "600s"/"downtime_jail_duration": "'${DOWNTIME_JAIL_DURATION}'"/' $DAEMON_HOME-1/config/genesis.json
sed -i 's/"unbonding_time": "1814400s"/"unbonding_time": "'${UNBONDING_PERIOD}'"/' $DAEMON_HOME-1/config/genesis.json

echo "[INFO]>> Distribute genesis.json of $IMAGE-1 to remaining nodes"
for (( a=2; a<=$NUM_VALS; a++ ))
do
    cp -v $DAEMON_HOME-1/config/genesis.json $PWD/localnet/$IMAGE-$a/config/
done

# updating config.toml
for (( a=1; a<=$NUM_VALS; a++ ))
do
    echo "INFO: Updating validator-$a chain config"
    sed -i 's#tcp://127.0.0.1:26657#tcp://0.0.0.0:26657#g' $DAEMON_HOME-$a/config/config.toml
    sed -i '/allow_duplicate_ip =/c\allow_duplicate_ip = true' $DAEMON_HOME-$a/config/config.toml
    sed -i '/pprof_laddr =/c\# pprof_laddr = "localhost:6060"' $DAEMON_HOME-$a/config/config.toml
    sed -i '/max_num_inbound_peers =/c\max_num_inbound_peers = 140' $DAEMON_HOME-$a/config/config.toml
    sed -i '/max_num_outbound_peers =/c\max_num_outbound_peers = 110' $DAEMON_HOME-$a/config/config.toml
    sed -i '/skip_timeout_commit = false/c\skip_timeout_commit = true' $DAEMON_HOME-$a/config/config.toml
done

chmod +x ./scripts/update_peers.sh
cp ./scripts/update_peers.sh ./localnet
chmod +x ./localnet/update_peers.sh

docker run -it -e DAEMON="$DAEMON" -e NUM_VALS=$NUM_VALS -e IMAGE="$IMAGE" -v $PWD/localnet:/localnet --rm $IMAGE bash -c "/localnet/update_peers.sh"

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

## Creating the docker-compose.yaml
yq eval-all '... comments=""|. as $item ireduce ({}; . * $item)|sort_keys(..)' /tmp/$IMAGE-*.yaml > $IMAGE-docker-compose.yaml
yq eval-all '... comments=""|. as $item ireduce ({}; . * $item)|sort_keys(..)' mongo-dc-template.yaml $IMAGE-docker-compose.yaml > docker-compose.yaml

echo "docker-compose file creation is done
Use : $ docker-compose up 
It will spin the all nodes
-------------------------------------------------------------
JSON RPC : http://localhost:26657
API      : http://localhost:1317
-------------------------------------------------------------
"