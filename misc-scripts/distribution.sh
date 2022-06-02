#/bin/sh

## This script executes distribuition module transactions like withdraw-rewards,
## withdraw-commission and withdraw-all-rewards.

# get absolute parent directory path of current file
CURPATH=`dirname $(realpath "$0")`
cd $CURPATH

# set environment with env config.
set -a
source ../env
set +a

# check environment variables are set
bash ../deps/env-check.sh $CURPATH

# NUM_VALS represents number of validator nodes
NUM_VALS=$1
if [ -z $NUM_VALS ]
then
    NUM_VALS=2
fi

echo "INFO: Number of validator nodes : $NUM_VALS"

IP="$(dig +short myip.opendns.com @resolver1.opendns.com)"
if [ -z $IP ]
then
    IP=127.0.0.1
fi

echo "--------- Run withdraw rewards tx -----------"

for (( a=1; a<=$NUM_VALS; a++ ))
do
    DIFF=`expr $a - 1`
    INC=`expr $DIFF \* 2`
    PORT=`expr 16657 + $INC`
    RPC="http://${IP}:${PORT}"
    validator=$("${DAEMON}" keys show validator${a} --bech val --keyring-backend test --home $DAEMON_HOME-${a} --output json)
    VALADDRESS=$(echo "${validator}" | jq -r '.address')
    FROMKEY="validator${a}"
    echo "validator address :: $VALADDRESS and from k1ey :: $FROMKEY"
    echo "Iteration no $a and values of address : $VALADDRESS and key : $FROMKEY"
    echo "--------- withdraw-rewards of $FROMKEY-----------"
    wrTx=$("${DAEMON}" tx distribution withdraw-rewards "${VALADDRESS}" --from $FROMKEY --fees 1000"${DENOM}" --chain-id "${CHAINID}" --keyring-backend test --home $DAEMON_HOME-${a} --node $RPC --output json -y)
    sleep 6s
    wrtxHash=$(echo "${wrTx}" | jq -r '.txhash')
    echo "TX HASH :: $wrtxHash"
    txResult=$("${DAEMON}" q tx "${wrtxHash}" --node $RPC --output json)
    wrCode=$(echo "${txResult}"| jq -r '.code')

    if [ "$wrCode" -eq 0 ]
    then
        echo "SUCCESS: withdraw-rewards of ( $VALADDRESS and key $FROMKEY ) is successfull and txHash is : $wrtxHash"
    else 
        echo "FAILED: withdraw-rewards of ( $VALADDRESS and key $FROMKEY ) failed and txHash is : $wrtxHash and REASON : $(echo "${wrTx}" | jq '.raw_log')"
    fi

done
echo "--------- Run withdraw-rewards commission txs -----------"
for (( a=1; a<=$NUM_VALS; a++ ))
do
    DIFF=`expr $a - 1`
    INC=`expr $DIFF \* 2`
    PORT=`expr 16657 + $INC` 
    RPC="http://${IP}:${PORT}"
    echo "NODE :: $RPC"
    validator=$("${DAEMON}" keys show validator${a} --bech val --keyring-backend test --home $DAEMON_HOME-${a} --output json)
    VALADDRESS=$(echo "${validator}" | jq -r '.address')
    FROMKEY="validator${a}"
    echo "validator address :: $VALADDRESS and From key :: $FROMKEY"
    echo "Iteration no $a and values of address : $VALADDRESS and key : $FROMKEY"
    echo "--------- withdraw-rewards commission of $FROMKEY-----------"
    wrcTx=$("${DAEMON}" tx distribution withdraw-rewards "${VALADDRESS}" --from $FROMKEY --commission --fees 1000"${DENOM}" --chain-id "${CHAINID}" --keyring-backend test --home $DAEMON_HOME-${a} --node $RPC --output json -y)
    sleep 6s
    wrctxHash=$(echo "${wrcTx}" | jq -r '.txhash')
    echo "TX HASH :: $wrctxHash"
    txResult=$("${DAEMON}" q tx "${wrctxHash}" --node $RPC --output json)
    wrcCode=$(echo "${txResult}"| jq -r '.code')
    
    if [ "$wrcCode" -eq 0 ]
    then
        echo "SUCCESS: withdraw-rewards commission of ( $VALADDRESS and key $FROMKEY ) is successfull and txHash is : $wrctxHash"
    else 
        echo "FAILED: withdraw-rewards comission of ( $VALADDRESS and key $FROMKEY ) failed and txHash is : $wrctxHash and REASON : $(echo "${wrcTx}" | jq '.raw_log')"
    fi
done

echo "--------- Run withdraw-all-rewards tx -----------"

for (( a=1; a<=$NUM_VALS; a++ ))
do
    DIFF=`expr $a - 1`
    INC=`expr $DIFF \* 2`
    PORT=`expr 16657 + $INC`
    RPC="http://${IP}:${PORT}"
    validator=$("${DAEMON}" keys show validator${a} --bech val --keyring-backend test --home $DAEMON_HOME-${a} --output json)
    VALADDRESS=$(echo "${validator}" | jq -r '.address')
    FROMKEY="validator${a}"
    echo "validator address :: $VALADDRESS and From key :: $FROMKEY"
    echo "Iteration no $a and values of address : $VALADDRESS and key : $FROMKEY"
    echo "------ withdraw-all-rewards of $FROMKEY --------"
    wartx=$($DAEMON tx distribution withdraw-all-rewards --from $FROMKEY --fees 1000"${DENOM}" --chain-id $CHAINID --keyring-backend test --home $DAEMON_HOME-${a} --node $RPC --output json -y)
    sleep 6s
    wartxHash=$(echo "${wartx}" | jq -r '.txhash')
    echo "TX HASH :: $wartxHash"
    txResult=$("${DAEMON}" q tx "${wartxHash}" --node $RPC --output json)
    warcode=$(echo "${txResult}"| jq -r '.code')

    if [ "$warcode" -eq 0 ];
    then
        echo "SUCCESS: withdraw-all-rewards of ( $VALADDRESS and key $FROMKEY ) is successfull and txHash is : $wartxHash"
    else 
        echo "FAILED: withdraw-all-rewards of ( $VALADDRESS and key $FROMKEY ) failed and txHash is $wartxHash and REASON : $(echo "${wartx}" | jq -r '.raw_log')"
    fi
    
done
