#/bin/sh

## This script executes staking module txs like delegate, redelegate and unbond.

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

echo "--------- Delegation tx -----------"
for (( a=1; a<$NUM_VALS; a++ ))
do
    DIFF=`expr $a - 1`
    INC=`expr $DIFF \* 2`
    PORT=`expr 16657 + $INC` 
    RPC="http://${IP}:${PORT}"
    TONODE=`expr 1 + $a`
    validator=$("${DAEMON}" keys show "validator${TONODE}" --bech val --keyring-backend test --home $DAEMON_HOME-${TONODE} --output json)
    VALADDRESS=$(echo "${validator}" | jq -r '.address')
    FROMKEY="validator${a}"
    TO=$VALADDRESS
    TOKEY="validator${TONODE}"
    echo "to validator address :: $TO and from key :: $FROMKEY"
    echo "Iteration no $a and values of from : $FROMKEY to : $TO"
    echo "--------- Delegation from $FROMKEY to $TO-----------"
    dTx=$("${DAEMON}" tx staking delegate "${TO}" 10000"${DENOM}" --from $FROMKEY --fees 1000"${DENOM}" --chain-id "${CHAINID}" --keyring-backend test --home $DAEMON_HOME-${a} --node $RPC --output json -y)
    sleep 6s
    dtxHash=$(echo "${dTx}" | jq -r '.txhash')
    echo "TX HASH :: $dtxHash **"
    txResult=$("${DAEMON}" q tx "${dtxHash}" --node $RPC --output json)
    dTxCode=$(echo "${txResult}"| jq -r '.code')

    if [ "$dTxCode" -eq 0 ];
    then
        echo "SUCCESS: Delegation from $FROMKEY to $TOKEY is SUCCESSFULL and txHash is : $dtxHash"
    else 
        echo "FAILED: Delegation from $FROMKEY to $TOKEY has FAILED and txHash is : $dtxHash and REASON : $(echo "${dTx}" | jq '.raw_log')"
    fi
    echo
done

echo "-----------Redelegation txs-------------"

for (( a=$NUM_VALS; a>=1; a-- ))
do
    if [ $a == 1 ]
    then
        N=$NUM_VALS
        P=`expr $NUM_VALS - 1`
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
        PORT=`expr 16657 + $INC` 
        RPC="http://${IP}:${PORT}"
        TONODE=`expr $a - 1`
        fromValidator=$("${DAEMON}" keys show "validator${a}" --bech val --keyring-backend test --home $DAEMON_HOME-${a} --output json)
        FROMADDRESS=$(echo "${fromValidator}" | jq -r '.address')
        toValidator=$("${DAEMON}" keys show "validator${TONODE}" --bech val --keyring-backend test --home $DAEMON_HOME-${TONODE} --output json)
        TOADDRESS=$(echo "${toValidator}" | jq -r '.address')
        FROM=$FROMADDRESS
        TO=$TOADDRESS
        FROMKEY="validator${a}"
        TOKEY="validator${TONODE}"
        echo "validator address :: $VALADDRESS and from key :: $FROMKEY"
    fi

    echo "Iteration no $a and values of from : $FROMKEY to : $TOKEY"
    echo "--------- Redelegation from $FROM to $TO-----------"
    rdTx=$("${DAEMON}" tx staking redelegate "${FROM}" "${TO}" 10000"${DENOM}" --from "${FROMKEY}" --fees 1000"${DENOM}" --gas 400000 --chain-id "${CHAINID}" --keyring-backend test --home $DAEMON_HOME-${a} --node $RPC --output json -y)
    sleep 6s
    rdtxHash=$(echo "${rdTx}" | jq -r '.txhash')
    echo "TX HASH :: $rdtxHash"
    txResult=$("${DAEMON}" q tx "${rdtxHash}" --node $RPC --output json)
    rdTxCode=$(echo "${txResult}"| jq -r '.code')

    if [ "$rdTxCode" -eq 0 ];
    then
        echo "SUCCESS: Redelegation from $FROMKEY to $TOKEY is SUCCESSFULL and txHash is : $rdtxHash"
    else 
        echo "FAILED: Redelegation from $FROMKEY to $TOKEY has FAILED and txHash is : $rdtxHash and REASON : $(echo "${rdTx}" | jq '.raw_log')"
    fi
done
echo "--------- Unbond txs -----------"
for (( a=1; a<$NUM_VALS; a++ ))
do
    DIFF=`expr $a - 1`
    INC=`expr $DIFF \* 2`
    PORT=`expr 16657 + $INC`
    RPC="http://${IP}:${PORT}"
    validator=$("${DAEMON}" keys show "validator${a}" --bech val --keyring-backend test --home $DAEMON_HOME-${a} --output json)
    VALADDRESS=$(echo "${validator}" | jq -r '.address')
    FROM=${VALADDRESS}
    FROMKEY="validator${a}"
    echo "validator address :: $FROM and From key :: $FROMKEY"
    echo "Iteration no $a and values of from : $FROM and fromKey : $FROMKEY"
    echo "--------- Running unbond tx command of $FROM and key : $FROMKEY------------"
    ubTx=$("${DAEMON}" tx staking unbond "${FROM}" 10000"${DENOM}" --from "${FROMKEY}" --fees 1000"${DENOM}" --chain-id "${CHAINID}" --keyring-backend test --home $DAEMON_HOME-${a} --node $RPC --output json -y)
    sleep 6s
    ubtxHash=$(echo "${ubTx}" | jq -r '.txhash')
    echo "TX HASH :: $ubtxHash"
    txResult=$("${DAEMON}" q tx "${ubtxHash}" --node $RPC --output json)
    ubTxCode=$(echo "${txResult}"| jq -r '.code')
    
    if [ "$ubTxCode" -eq 0 ];
    then
        echo "SUCCESS: Unbond tx ( of $FROM and key $FROMKEY ) is SUCCESSFULL and txHash is : $ubtxHash"
    else 
        echo "FAILED: Unbond tx ( of $FROM and key $FROMKEY ) FAILED and txHash is : $ubtxHash  and REASON : $(echo "${ubTx}" | jq '.raw_log')"
    fi

done
