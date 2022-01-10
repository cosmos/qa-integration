#/bin/sh

# read no.of nodes to be setup
NODES=$1
if [ -z $NODES ]
then
    NODES=2
fi

# read no of accounts to be setup
ACCOUNTS=$2
echo " ** Number of nodes : $NODES and accounts : $ACCOUNTS to be setup **"
echo "**** Number of nodes to be setup: $NODES ****"
cd $HOME
echo "--------- Install cosmovisor-------"
go install github.com/cosmos/cosmos-sdk/cosmovisor/cmd/cosmovisor@v1.0.0
strings $(which cosmovisor) | egrep -e "mod\s+github.com/cosmos/cosmos-sdk/cosmovisor"
export REPO=$(basename $GH_URL .git)
echo "--------- Install $DAEMON ---------"
git clone $GH_URL && cd $REPO
git fetch && git checkout $CHAIN_VERSION
make install
cd $HOME
# check version
$DAEMON version --long
# export daemon home paths
for (( a=1; a<=$NODES; a++ ))
do
    export DAEMON_HOME_$a=$DAEMON_HOME-$a
    echo "Deamon path :: $DAEMON_HOME-$a"
    $DAEMON unsafe-reset-all  --home $DAEMON_HOME-$a
    echo "****** here command $DAEMON unsafe-reset-all  --home $DAEMON_HOME-$a ******"
done
# remove daemon home directories if it already exists
for (( a=1; a<=$NODES; a++ ))
do
    rm -rf $DAEMON_HOME-$a
done
echo "-----Creating daemon home directories------"
for (( a=1; a<=$NODES; a++ ))
do
    echo "****** create dir :: $DAEMON_HOME-$a ********"
    mkdir -p "$DAEMON_HOME-$a"
    mkdir -p "$DAEMON_HOME-$a"/cosmovisor/genesis/bin
    cp $(which $DAEMON) "$DAEMON_HOME-$a"/cosmovisor/genesis/bin/
done
echo "--------Start initializing the chain ($CHAINID)---------"
for (( a=1; a<=$NODES; a++ ))
do
    echo "-------Init chain ${a}--------"
    echo "Deamon home :: $DAEMON_HOME-${a}"
    $DAEMON init --chain-id $CHAINID $DAEMON_HOME-${a} --home $DAEMON_HOME-${a}
done
echo "---------Creating $NODES keys-------------"
for (( a=1; a<=$NODES; a++ ))
do
    $DAEMON keys add "validator${a}" --keyring-backend test --home $DAEMON_HOME-${a}
done

# add accounts if second argument is passed
if [ -z $ACCOUNTS ] || [ "$ACCOUNTS" -eq 0 ]
then
    echo "----- Argument for accounts is not present, not creating any additional accounts --------"
else
    echo "---------Creating $ACCOUNTS accounts-------------"
    for (( a=1; a<=$ACCOUNTS; a++ ))
    do
        $DAEMON keys add "account${a}" --keyring-backend test --home $DAEMON_HOME-1
    done
fi

echo "----------Genesis creation---------"
for (( a=1; a<=$NODES; a++ ))
do
    if [ $a == 1 ]
    then
        $DAEMON --home $DAEMON_HOME-$a add-genesis-account validator$a 1000000000000$DENOM  --keyring-backend test
        echo "done $DAEMON_HOME-$a genesis creation "
        continue
    fi
    $DAEMON --home $DAEMON_HOME-$a add-genesis-account validator$a 1000000000000$DENOM  --keyring-backend test
    $DAEMON --home $DAEMON_HOME-1 add-genesis-account $($DAEMON keys show validator$a -a --home $DAEMON_HOME-$a --keyring-backend test) 1000000000000$DENOM
done
echo "----------Genesis creation for accounts---------"

if [ -z $ACCOUNTS ]
then
    echo "Second argument was empty, so not setting up any account\n"
else
    for (( a=1; a<=$ACCOUNTS; a++ ))
    do
        echo "cmd ::$DAEMON --home $DAEMON_HOME-1 add-genesis-account $($DAEMON keys show account$a -a --home $DAEMON_HOME-1 --keyring-backend test) 1000000000000$DENOM"
        $DAEMON --home $DAEMON_HOME-1 add-genesis-account $($DAEMON keys show account$a -a --home $DAEMON_HOME-1 --keyring-backend test) 1000000000000$DENOM
    done
fi

echo "--------Gentx--------"
for (( a=1; a<=$NODES; a++ ))
do
    $DAEMON gentx validator$a 90000000000$DENOM --chain-id $CHAINID  --keyring-backend test --home $DAEMON_HOME-$a
done
echo "---------Copy all gentxs to $DAEMON_HOME-1----------"
for (( a=2; a<=$NODES; a++ ))
do
    cp $DAEMON_HOME-$a/config/gentx/*.json $DAEMON_HOME-1/config/gentx/
done
echo "----------collect-gentxs------------"
$DAEMON collect-gentxs --home $DAEMON_HOME-1
echo "---------Updating $DAEMON_HOME-1 genesis.json ------------"
sed -i "s/172800000000000/600000000000/g" $DAEMON_HOME-1/config/genesis.json
sed -i "s/172800s/600s/g" $DAEMON_HOME-1/config/genesis.json
sed -i "s/stake/$DENOM/g" $DAEMON_HOME-1/config/genesis.json
echo "---------Distribute genesis.json of $DAEMON_HOME-1 to remaining nodes-------"
for (( a=2; a<=$NODES; a++ ))
do
    cp $DAEMON_HOME-1/config/genesis.json $DAEMON_HOME-$a/config/
done
echo "---------Getting public IP address-----------"
IP="$(dig +short myip.opendns.com @resolver1.opendns.com)"

if [ -z $IP ]
then
    IP=127.0.0.1
fi

for (( a=1; a<=$NODES; a++ ))
do
    DIFF=`expr $a - 1`
    INC=`expr $DIFF \* 2`
    LADDR=`expr 16656 + $INC` 
    echo "----------Get node-id of $DAEMON_HOME-$a ---------"
    nodeID=$("${DAEMON}" tendermint show-node-id --home $DAEMON_HOME-$a)
    echo "** Node ID :: $nodeID **"
    PR="$nodeID@$IP:$LADDR"
    if [ $a == 1 ]
    then
        PERSISTENT_PEERS="${PR}"
        continue
    fi
    PERSISTENT_PEERS="${PERSISTENT_PEERS},${PR}"
done
#updating config.toml
for (( a=1; a<=$NODES; a++ ))
do
    DIFF=`expr $a - 1`
    INC=`expr $DIFF \* 2`
    RPC=`expr 16657 + $INC` #increment rpc ports
    LADDR=`expr 16656 + $INC` #increment laddr ports
    GRPC=`expr 9090 + $INC` #increment grpc poprt
    WGRPC=`expr 9091 + $INC` #increment web grpc port
    echo "----------Updating $DAEMON_HOME-$a chain config-----------"
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
#create system services
for (( a=1; a<=$NODES; a++ ))
do
    DIFF=`expr $a - 1`
    INC=`expr $DIFF \* 2`
    RPC=`expr 16657 + $INC`
    echo "---------Creating $DAEMON_HOME-$a system file---------"
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
    echo "-------Starting $DAEMON-${a} service-------"
    sudo -S systemctl daemon-reload
    sudo -S systemctl start $DAEMON-${a}.service
    sleep 1s
    echo "Checking $DAEMON_HOME-${a} chain status"
    $DAEMON status --node tcp://localhost:${RPC}
done