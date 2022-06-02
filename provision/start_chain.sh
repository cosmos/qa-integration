#/bin/sh

## This script sets up a multinode network and generates multilple addresses with 
## balance for testing purposes.

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

# NUM_VALS represents number of validator nodes to bootstrap the network.
NUM_VALS=$1
if [ -z $NUM_VALS ]
then
    NUM_VALS=2
fi

# NUM_ACCOUNTS represents number of accounts to initialize while bootstropping the chain. 
# These are the additional accounts along with the validator accounts.
NUM_ACCOUNTS=$2
echo "INFO: Setting up $NUM_NODES validator nodes and $NUM_ACCOUNTS accounts"
cd $HOME
echo "INFO: Installing cosmovisor"
go install github.com/cosmos/cosmos-sdk/cosmovisor/cmd/cosmovisor@v1.0.0
strings $(which cosmovisor) | egrep -e "mod\s+github.com/cosmos/cosmos-sdk/cosmovisor"
export REPO=$(basename $GH_URL .git)

echo "INFO: Installing $DAEMON"
CURR_VERSION='v'$($DAEMON version)
if [ $CURR_VERSION != $CHAIN_VERSION ]
then
    if [ ! -d $REPO ]
    then
        git clone $GH_URL
    fi
    cd $REPO
    git fetch --all && git checkout $CHAIN_VERSION
    make install
fi
cd $HOME
# check version
$DAEMON version --long
# export daemon home paths
for (( a=1; a<=$NUM_VALS; a++ ))
do
    export DAEMON_HOME_$a=$DAEMON_HOME-$a
done
# remove validator daemon home directories if they already exist
for (( a=1; a<=$NUM_VALS; a++ ))
do
    rm -rf $DAEMON_HOME-$a
done
echo "INFO: Setting up validator home directories"
for (( a=1; a<=$NUM_VALS; a++ ))
do
    echo "INFO: Creating validator-$a home directory :: $DAEMON_HOME-$a"
    mkdir -p "$DAEMON_HOME-$a"
    mkdir -p "$DAEMON_HOME-$a"/cosmovisor/genesis/bin
    cp $(which $DAEMON) "$DAEMON_HOME-$a"/cosmovisor/genesis/bin/
done
echo "INFO: Initializing the chain ($CHAINID)"
for (( a=1; a<=$NUM_VALS; a++ ))
do
    echo "INFO: Initializing validator-${a} configuration files"
    $DAEMON init --chain-id $CHAINID validator-${a} --home $DAEMON_HOME-${a}
done
echo "---------Creating $NUM_VALS keys-------------"
for (( a=1; a<=$NUM_VALS; a++ ))
do
    $DAEMON keys add "validator${a}" --keyring-backend test --home $DAEMON_HOME-${a}
done

# create accounts if second argument is passed
if [ -z $NUM_ACCOUNTS ] || [ "$NUM_ACCOUNTS" -eq 0 ]
then
    echo "INFO: Second argument was empty, not setting up additional account"
else
    echo "INFO: Creating $NUM_ACCOUNTS additional accounts"
    for (( a=1; a<=$NUM_ACCOUNTS; a++ ))
    do
        $DAEMON keys add "account${a}" --keyring-backend test --home $DAEMON_HOME-1
    done
fi

echo "INFO: Setting up genesis"
echo "INFO: Adding validator accounts to genesis"
for (( a=1; a<=$NUM_VALS; a++ ))
do
    if [ $a == 1 ]
    then
        $DAEMON --home $DAEMON_HOME-$a add-genesis-account validator$a 1000000000000$DENOM  --keyring-backend test
        echo "INFO: Done $DAEMON_HOME-$a genesis creation "
        continue
    fi
    $DAEMON --home $DAEMON_HOME-$a add-genesis-account validator$a 1000000000000$DENOM  --keyring-backend test
    $DAEMON --home $DAEMON_HOME-1 add-genesis-account $($DAEMON keys show validator$a -a --home $DAEMON_HOME-$a --keyring-backend test) 1000000000000$DENOM
done
echo "INFO: Adding additional accounts to genesis"
if [ -z $NUM_ACCOUNTS ]
then
    echo "INFO: Second argument was empty, not setting up additional account"
else
    for (( a=1; a<=$NUM_ACCOUNTS; a++ ))
    do
        $DAEMON --home $DAEMON_HOME-1 add-genesis-account $($DAEMON keys show account$a -a --home $DAEMON_HOME-1 --keyring-backend test) 1000000000000$DENOM
    done
fi

echo "INFO: Generating gentxs for validator accounts"
for (( a=1; a<=$NUM_VALS; a++ ))
do
    $DAEMON gentx validator$a 90000000000$DENOM --chain-id $CHAINID  --keyring-backend test --home $DAEMON_HOME-$a
done
echo "INFO: Copying all gentxs to $DAEMON_HOME-1"
for (( a=2; a<=$NUM_VALS; a++ ))
do
    cp $DAEMON_HOME-$a/config/gentx/*.json $DAEMON_HOME-1/config/gentx/
done
echo "INFO: Collecting gentxs"
$DAEMON collect-gentxs --home $DAEMON_HOME-1
echo "INFO: Updating genesis values"
sed -i "s/172800000000000/600000000000/g" $DAEMON_HOME-1/config/genesis.json
sed -i "s/172800s/600s/g" $DAEMON_HOME-1/config/genesis.json
sed -i "s/stake/$DENOM/g" $DAEMON_HOME-1/config/genesis.json
echo "INFO: Distribute genesis.json of validator-1 to remaining nodes"
for (( a=2; a<=$NUM_VALS; a++ ))
do
    cp $DAEMON_HOME-1/config/genesis.json $DAEMON_HOME-$a/config/
done

echo "INFO: Getting public IP address to configure peers"
IP="$(dig +short myip.opendns.com @resolver1.opendns.com)"
if [ -z $IP ]
then
    IP=127.0.0.1
fi

for (( a=1; a<=$NUM_VALS; a++ ))
do
    DIFF=$(($a - 1))
    INC=$(($DIFF * 2))
    LADDR=$((16656 + $INC))
    echo "INFO: Getting node-id of validator-$a"
    nodeID=$("${DAEMON}" tendermint show-node-id --home $DAEMON_HOME-$a)
    PR="$nodeID@$IP:$LADDR"
    if [ $a == 1 ]
    then
        PERSISTENT_PEERS="${PR}"
        continue
    fi
    PERSISTENT_PEERS="${PERSISTENT_PEERS},${PR}"
done
# updating config.toml
for (( a=1; a<=$NUM_VALS; a++ ))
do
    DIFF=$(($a - 1))
    INC=$(($DIFF * 2))
    RPC=$((16657 + $INC)) #increment rpc ports
    LADDR=$((16656 + $INC)) #increment laddr ports
    GRPC=$((9090 + $INC)) #increment grpc poprt
    WGRPC=$((9091 + $INC)) #increment web grpc port
    echo "INFO: Updating validator-$a chain config"
    sed -i 's#tcp://127.0.0.1:26657#tcp://0.0.0.0:'${RPC}'#g' $DAEMON_HOME-$a/config/config.toml
    sed -i 's#tcp://0.0.0.0:26656#tcp://0.0.0.0:'${LADDR}'#g' $DAEMON_HOME-$a/config/config.toml
    sed -i '/persistent_peers =/c\persistent_peers = "'"$PERSISTENT_PEERS"'"' $DAEMON_HOME-$a/config/config.toml
    sed -i '/allow_duplicate_ip =/c\allow_duplicate_ip = true' $DAEMON_HOME-$a/config/config.toml
    sed -i '/pprof_laddr =/c\# pprof_laddr = "localhost:6060"' $DAEMON_HOME-$a/config/config.toml
    sed -i 's#0.0.0.0:9090#0.0.0.0:'${GRPC}'#g' $DAEMON_HOME-$a/config/app.toml
    sed -i 's#0.0.0.0:9091#0.0.0.0:'${WGRPC}'#g' $DAEMON_HOME-$a/config/app.toml
    sed -i '/max_num_inbound_peers =/c\max_num_inbound_peers = 140' $DAEMON_HOME-$a/config/config.toml
    sed -i '/max_num_outbound_peers =/c\max_num_outbound_peers = 110' $DAEMON_HOME-$a/config/config.toml
done
# create systemd service files
for (( a=1; a<=$NUM_VALS; a++ ))
do
    DIFF=$(($a - 1))
    INC=$(($DIFF * 2))
    RPC=$((16657 + $INC))
    echo "INFO: Creating $DAEMON-$a systemd service file"
    echo "[Unit]
    Description=${DAEMON} daemon
    After=network.target
    [Service]
    Environment="DAEMON_HOME=$DAEMON_HOME-$a"
	Environment="DAEMON_NAME=$DAEMON"
	Environment="DAEMON_ALLOW_DOWNLOAD_BINARIES=false"
	Environment="DAEMON_RESTART_AFTER_UPGRADE=true"
	Environment="UNSAFE_SKIP_BACKUP=false"
    Type=simple
    User=$USER
    ExecStart=$(which cosmovisor) start --home $DAEMON_HOME-$a
    Restart=on-failure
    RestartSec=3
    LimitNOFILE=4096
    [Install]
    WantedBy=multi-user.target" | sudo tee "/lib/systemd/system/$DAEMON-${a}.service"
    echo "INFO: Starting $DAEMON-${a} service"
    sudo -S systemctl daemon-reload
    sudo -S systemctl start $DAEMON-${a}.service
    sleep 1s
    echo "INFO: Checking $DAEMON_HOME-${a} chain status"
    $DAEMON status --node tcp://localhost:${RPC}
done