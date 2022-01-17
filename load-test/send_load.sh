#/bin/sh

FROM=$1
if [ -z $FROM ]
then
    FROM=1
fi

TO=$2
if [ -z $TO ]
then
    TO=2
fi

IP="$(dig +short myip.opendns.com @resolver1.opendns.com)"
echo "Public IP address: ${IP}"
PORT=16657

if [ -z $IP ]
then
    IP=127.0.0.1
    PORT=16657
fi

RPC="http://${IP}:${PORT}"
acc1=$($DAEMON keys show account$FROM -a --home $DAEMON_HOME-1 --keyring-backend test)
acc2=$($DAEMON keys show account$TO -a --home $DAEMON_HOME-1 --keyring-backend test)
seq1=$("${DAEMON}" q account "${acc1}" --node $RPC --output json)
seq2=$("${DAEMON}" q account "${acc2}" --node $RPC --output json)
seq1no=$(echo "${seq1}" | jq -r '.sequence')
seq2no=$(echo "${seq2}" | jq -r '.sequence')
balance1=$("${DAEMON}" q bank balances "${acc1}" --node $RPC --output json)
balance1res=$(echo "${balance1}" | jq -r '.balances')
echo "** Balance of Account 1 before send_load :: $balance1res **"
balance2=$("${DAEMON}" q bank balances "${acc2}" --node $RPC --output json)
balance2res=$(echo "${balance1}" | jq -r '.balances')
echo "** Balance of Account 2 before send_load :: $balance2res **"
bound1=`expr 10000 + $seq1no`
bound2=`expr 10000 + $seq2no`
for (( a=$seq1no; a<$bound1; a++ ))
do
    sTx=$("${DAEMON}" tx bank send "${acc1}" "${acc2}" 1000000"${DENOM}" --chain-id "${CHAINID}" --keyring-backend test --home $DAEMON_HOME-1 --node $RPC --output json -y --sequence $a) 
    sTxHash=$(echo "${sTx}" | jq -r '.txhash')
    echo "** TX HASH :: $sTxHash **"
done

for (( a=$seq2no; a<$bound2; a++ ))
do
    sTx=$("${DAEMON}" tx bank send "${acc2}" "${acc1}" 1000000"${DENOM}" --chain-id "${CHAINID}" --keyring-backend test --home $DAEMON_HOME-1 --node $RPC --output json -y --sequence $a) 
    sTxHash=$(echo "${sTx}" | jq -r '.txhash')
    echo "** TX HASH :: $sTxHash **"
done

balance1=$("${DAEMON}" q bank balances "${acc1}" --node $RPC --output json)
balance1res=$(echo "${balance1}" | jq -r '.balances')
echo "** Balance of Account 1 after send_load :: $balance1res **"
balance2=$("${DAEMON}" q bank balances "${acc2}" --node $RPC --output json)
balance2res=$(echo "${balance1}" | jq -r '.balances')
echo "** Balance of Account 2 after send_load :: $balance2res **"