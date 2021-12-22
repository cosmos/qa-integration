#/bin/sh

display_usage() {
    printf "** Please check the exported values:: **\n Deamon : $DEAMON\n Denom : $DENOM\n ChainID : $CHAINID\n Daemon home : $DAEMON_HOME\n"
    exit 1
}

if [ -z $DAEMON ] || [ -z $DENOM ] || [ -z $CHAINID ] || [ -z $DAEMON_HOME ]
then 
    display_usage
fi

echo

# read no.of nodes
NODES=$1
NODES=$1
if [ -z $NODES ]
then
    NODES=2
fi

echo

echo "** Number of nodes mentioned : $NODES **"

IP="$(dig +short myip.opendns.com @resolver1.opendns.com)"
echo "Public IP address: ${IP}"

if [ -z $IP ]
then
    IP=127.0.0.1
fi

echo "--------- Delegation tx -----------"

for (( a=1; a<$NODES; a++ ))
do
    DIFF=`expr $a - 1`
    INC=`expr $DIFF \* 2`
    PORT=`expr 16657 + $INC` #get ports
    RPC="http://${IP}:${PORT}"
    echo "NODE :: $RPC"

    TONODE=`expr 1 + $a`
    echo "To node number : $TONODE"

    validator=$("${DAEMON}" keys show "validator${TONODE}" --bech val --keyring-backend test --home $DAEMON_HOME-${TONODE} --output json)
    VALADDRESS=$(echo "${validator}" | jq -r '.address')

    FROMKEY="validator${a}"
    TO=$VALADDRESS
    TOKEY="validator${TONODE}"

    echo "** to validator address :: $TO and from key :: $FROMKEY **"
    # Print the value
    echo "Iteration no $a and values of from : $FROMKEY to : $TO"
    echo "--------- Delegation from $FROMKEY to $TO-----------"

    dTx=$("${DAEMON}" tx staking delegate "${TO}" 10000"${DENOM}" --from $FROMKEY --fees 1000"${DENOM}" --chain-id "${CHAINID}" --keyring-backend test --home $DAEMON_HOME-${a} --node $RPC --output json -y)
    
    sleep 6s

    dtxHash=$(echo "${dTx}" | jq -r '.txhash')
    echo "** TX HASH :: $dtxHash **"

    # query the txhash and check the code
    txResult=$("${DAEMON}" q tx "${dtxHash}" --node $RPC --output json)
    dTxCode=$(echo "${txResult}"| jq -r '.code')

    echo "Code is : $dTxCode"
    echo
    if [ "$dTxCode" -eq 0 ];
    then
        echo "**** Delegation from $FROMKEY to $TOKEY is SUCCESSFULL!!  txHash is : $dtxHash ****"
    else 
        echo "**** Delegation from $FROMKEY to $TOKEY has FAILED!!!!   txHash is : $dtxHash and REASON : $(echo "${dTx}" | jq '.raw_log')***"
    fi
    echo
done

echo

echo "-----------Redelegation txs-------------"

for (( a=$NODES; a>=1; a-- ))
do

    if [ $a == 1 ]
    then
        # this tx has to fail as the tx between these nodes has already happened
        N=$NODES
        P=`expr $NODES - 1`
        fromValidator=$("${DAEMON}" keys show "validator${N}" --bech val --keyring-backend test --home $DAEMON_HOME-${N} --output json)
        FROMADDRESS=$(echo "${fromValidator}" | jq -r '.address')

        toValidator=$("${DAEMON}" keys show "validator${P}" --bech val --keyring-backend test --home $DAEMON_HOME-${P} --output json)
        TOADDRESS=$(echo "${toValidator}" | jq -r '.address')

        FROM=$FROMADDRESS
        TO=$TOADDRESS
        FROMKEY="validator${N}"
        TOKEY="validator${P}"
    else 
        DIFF=`expr $a - 1`
        INC=`expr $DIFF \* 2`
        PORT=`expr 16657 + $INC` #get ports
        RPC="http://${IP}:${PORT}"
        echo "NODE :: $RPC"

        TONODE=`expr $a - 1`
        echo "To node number : $TONODE"

        fromValidator=$("${DAEMON}" keys show "validator${a}" --bech val --keyring-backend test --home $DAEMON_HOME-${a} --output json)
        FROMADDRESS=$(echo "${fromValidator}" | jq -r '.address')

        toValidator=$("${DAEMON}" keys show "validator${TONODE}" --bech val --keyring-backend test --home $DAEMON_HOME-${TONODE} --output json)
        TOADDRESS=$(echo "${toValidator}" | jq -r '.address')

        FROM=$FROMADDRESS
        TO=$TOADDRESS
        FROMKEY="validator${a}"
        TOKEY="validator${TONODE}"
        echo "** validator address :: $VALADDRESS and from key :: $FROMKEY **"
    fi

    # Print the value
    echo "Iteration no $a and values of from : $FROMKEY to : $TOKEY"
    echo "--------- Redelegation from $FROM to $TO-----------"

    rdTx=$("${DAEMON}" tx staking redelegate "${FROM}" "${TO}" 10000"${DENOM}" --from "${FROMKEY}" --fees 1000"${DENOM}" --gas 400000 --chain-id "${CHAINID}" --keyring-backend test --home $DAEMON_HOME-${a} --node $RPC --output json -y)
    
    sleep 6s
    
    rdtxHash=$(echo "${rdTx}" | jq -r '.txhash')
    echo "** TX HASH :: $rdtxHash **"

    # query the txhash and check the code
    txResult=$("${DAEMON}" q tx "${rdtxHash}" --node $RPC --output json)
    rdTxCode=$(echo "${txResult}"| jq -r '.code')

    echo "Code is : $rdTxCode"
    echo
    if [ "$rdTxCode" -eq 0 ];
    then
        echo "**** Redelegation from $FROMKEY to $TOKEY is SUCCESSFULL!!  txHash is : $rdtxHash ****"
    else 
        echo "**** Redelegation from $FROMKEY to $TOKEY has FAILED!!!!   txHash is : $rdtxHash and REASON : $(echo "${rdTx}" | jq '.raw_log') ***"
    fi
    echo
done

echo


echo "--------- Unbond txs -----------"

for (( a=1; a<$NODES; a++ ))
do
    DIFF=`expr $a - 1`
    INC=`expr $DIFF \* 2`
    PORT=`expr 16657 + $INC` #get ports
    RPC="http://${IP}:${PORT}"
    echo "NODE :: $RPC"

    validator=$("${DAEMON}" keys show "validator${a}" --bech val --keyring-backend test --home $DAEMON_HOME-${a} --output json)
    VALADDRESS=$(echo "${validator}" | jq -r '.address')

    FROM=${VALADDRESS}
    FROMKEY="validator${a}"
    echo "** validator address :: $FROM and From key :: $FROMKEY **"

    # Print the value
    echo "Iteration no $a and values of from : $FROM and fromKey : $FROMKEY"
    echo "--------- Running unbond tx command of $FROM and key : $FROMKEY------------"

    ubTx=$("${DAEMON}" tx staking unbond "${FROM}" 10000"${DENOM}" --from "${FROMKEY}" --fees 1000"${DENOM}" --chain-id "${CHAINID}" --keyring-backend test --home $DAEMON_HOME-${a} --node $RPC --output json -y)
    
    sleep 6s
    
    ubtxHash=$(echo "${ubTx}" | jq -r '.txhash')
    echo "** TX HASH :: $ubtxHash **"

    # query the txhash and check the code
    txResult=$("${DAEMON}" q tx "${ubtxHash}" --node $RPC --output json)
    ubTxCode=$(echo "${txResult}"| jq -r '.code')

    echo "Code is : $ubTxCode"
    echo
    if [ "$ubTxCode" -eq 0 ];
    then
        echo "**** Unbond tx ( of $FROM and key $FROMKEY ) is SUCCESSFULL!!  txHash is : $ubtxHash ****"
    else 
        echo "**** Unbond tx ( of $FROM and key $FROMKEY ) FAILED!!!!   txHash is : $ubtxHash  and REASON : $(echo "${ubTx}" | jq '.raw_log')  ***"
    fi
    echo
done

echo
