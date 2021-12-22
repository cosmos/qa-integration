#/bin/sh

display_usage() {
    printf "** Please check the exported values:: **\n Daemon : $DAEMON\n Denom : $DENOM\n ChainID : $CHAINID\n Daemon home : $DAEMON_HOME\n"
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

echo "** Number of nodes mentioned : $NODES **"

IP="$(dig +short myip.opendns.com @resolver1.opendns.com)"
echo "Public IP address: ${IP}"

if [ -z $IP ]
then
    IP=127.0.0.1
fi

echo "--------- Run withdraw rewards tx -----------"

for (( a=1; a<=$NODES; a++ ))
do
    DIFF=`expr $a - 1`
    INC=`expr $DIFF \* 2`
    PORT=`expr 16657 + $INC` #get ports
    RPC="http://${IP}:${PORT}"
    echo "NODE :: $RPC"

    validator=$("${DAEMON}" keys show validator${a} --bech val --keyring-backend test --home $DAEMON_HOME-${a} --output json)
    VALADDRESS=$(echo "${validator}" | jq -r '.address')
    FROMKEY="validator${a}"
    echo "** validator address :: $VALADDRESS and From key :: $FROMKEY **"

    # Print the value
    echo "Iteration no $a and values of address : $VALADDRESS and key : $FROMKEY"
    echo "--------- withdraw-rewards of $FROMKEY-----------"

    wrTx=$("${DAEMON}" tx distribution withdraw-rewards "${VALADDRESS}" --from $FROMKEY --fees 1000"${DENOM}" --chain-id "${CHAINID}" --keyring-backend test --home $DAEMON_HOME-${a} --node $RPC --output json -y)
    sleep 6s

    wrtxHash=$(echo "${wrTx}" | jq -r '.txhash')

    echo "** TX HASH :: $wrtxHash **"

    # query the txhash and check the code
    txResult=$("${DAEMON}" q tx "${wrtxHash}" --node $RPC --output json)
    wrCode=$(echo "${txResult}"| jq -r '.code')

    echo "Code is : $wrCode"
    if [ "$wrCode" -eq 0 ]
    then
        echo "**** withdraw-rewards of ( $VALADDRESS and key $FROMKEY ) is successfull!!  txHash is : $wrtxHash ****"
    else 
        echo "**** withdraw-rewards of ( $VALADDRESS and key $FROMKEY ) failed!!!!   txHash is : $wrtxHash and REASON : $(echo "${wrTx}" | jq '.raw_log') ****"
    fi
done

echo

echo "--------- Run withdraw-rewards commission txs -----------"

for (( a=1; a<=$NODES; a++ ))
do
    DIFF=`expr $a - 1`
    INC=`expr $DIFF \* 2`
    PORT=`expr 16657 + $INC` #get ports
    RPC="http://${IP}:${PORT}"
    echo " **** NODE :: $RPC  ****"

    validator=$("${DAEMON}" keys show validator${a} --bech val --keyring-backend test --home $DAEMON_HOME-${a} --output json)
    VALADDRESS=$(echo "${validator}" | jq -r '.address')
    FROMKEY="validator${a}"
    echo "** validator address :: $VALADDRESS and From key :: $FROMKEY **"

     # Print the value
    echo "Iteration no $a and values of address : $VALADDRESS and key : $FROMKEY"
    echo "--------- withdraw-rewards commission of $FROMKEY-----------"

    wrcTx=$("${DAEMON}" tx distribution withdraw-rewards "${VALADDRESS}" --from $FROMKEY --commission --fees 1000"${DENOM}" --chain-id "${CHAINID}" --keyring-backend test --home $DAEMON_HOME-${a} --node $RPC --output json -y)
    #echo $wrTx
    sleep 6s

    wrctxHash=$(echo "${wrcTx}" | jq -r '.txhash')

    echo "** TX HASH :: $wrctxHash **"

    # query the txhash and check the code
    txResult=$("${DAEMON}" q tx "${wrctxHash}" --node $RPC --output json)
    wrcCode=$(echo "${txResult}"| jq -r '.code')
    
    echo "Code is : $wrcCode"
    if [ "$wrcCode" -eq 0 ]
    then
        echo "**** withdraw-rewards commission of ( $VALADDRESS and key $FROMKEY ) is successfull!!  txHash is : $wrctxHash ****"
    else 
        echo "**** withdraw-rewards comission of ( $VALADDRESS and key $FROMKEY ) failed!!!!   txHash is : $wrctxHash and REASON : $(echo "${wrcTx}" | jq '.raw_log') ****"
    fi
done

echo


echo "--------- Run withdraw-all-rewards tx -----------"

for (( a=1; a<=$NODES; a++ ))
do
    DIFF=`expr $a - 1`
    INC=`expr $DIFF \* 2`
    PORT=`expr 16657 + $INC` #get ports
    RPC="http://${IP}:${PORT}"
    echo "NODE :: $RPC"

    validator=$("${DAEMON}" keys show validator${a} --bech val --keyring-backend test --home $DAEMON_HOME-${a} --output json)
    VALADDRESS=$(echo "${validator}" | jq -r '.address')
    FROMKEY="validator${a}"
    echo "** validator address :: $VALADDRESS and From key :: $FROMKEY **"

    # Print the value
    echo "Iteration no $a and values of address : $VALADDRESS and key : $FROMKEY"
    echo "------ withdraw-all-rewards of $FROMKEY --------"

    wartx=$($DAEMON tx distribution withdraw-all-rewards --from $FROMKEY --fees 1000"${DENOM}" --chain-id $CHAINID --keyring-backend test --home $DAEMON_HOME-${a} --node $RPC --output json -y)
    sleep 6s

    wartxHash=$(echo "${wartx}" | jq -r '.txhash')

    echo "** TX HASH :: $wartxHash **"

     # query the txhash and check the code
    txResult=$("${DAEMON}" q tx "${wartxHash}" --node $RPC --output json)
    warcode=$(echo "${txResult}"| jq -r '.code')
    
    echo "Code is : $warcode"
    if [ "$warcode" -eq 0 ];
    then
        echo "**** withdraw-all-rewards of ( $VALADDRESS and key $FROMKEY ) is successfull!!  txHash is : $wartxHash ****"
    else 
        echo "**** withdraw-all-rewards of ( $VALADDRESS and key $FROMKEY ) failed!!!!   txHash is : $wartxHash and REASON : $(echo "${wartx}" | jq -r '.raw_log') ****"
    fi
done

echo
