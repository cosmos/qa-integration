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

balance_query() {
    balance=$("${DAEMON}" q bank balances $1 --node $RPC --output json)
    balanceres=$(echo "${balance}" | jq -r '.balances')
    return "$balanceres"
}

RPC="http://${IP}:${PORT}"
num_txs=1000
acc1=$($DAEMON keys show account$FROM -a --home $DAEMON_HOME-1 --keyring-backend test)
acc2=$($DAEMON keys show account$TO -a --home $DAEMON_HOME-1 --keyring-backend test)
echo "** Balance of Account 1 before send_load :: **"
balance_query "$acc1"
echo "** Balance of Account 2 before send_load :: **"
balance_query "$acc2"
cd ~/
seq1=$("${DAEMON}" q account "${acc1}" --node $RPC --output json)
seq1no=$(echo "${seq1}" | jq -r '.sequence')
seq2=$("${DAEMON}" q account "${acc2}" --node $RPC --output json)
seq2no=$(echo "${seq2}" | jq -r '.sequence')
for (( a=0; a<$num_txs; a++ ))
do
		seqto=$(expr $seq1no + $a)
		seqfrom=$(expr $seq2no + $a)
    sTx=$("${DAEMON}" tx bank send "${acc1}" "${acc2}" 1000000"${DENOM}" --chain-id "${CHAINID}" --keyring-backend test --home $DAEMON_HOME-1 --node $RPC --output json -y --sequence $seqto) 
    sTxHash=$(echo "${sTx}" | jq -r '.txhash')
    echo "** TX HASH :: $sTxHash **"
	  sTx=$("${DAEMON}" tx bank send "${acc2}" "${acc1}" 1000000"${DENOM}" --chain-id "${CHAINID}" --keyring-backend test --home $DAEMON_HOME-1 --node $RPC --output json -y --sequence $seqfrom) 
    sTxHash=$(echo "${sTx}" | jq -r '.txhash')
    echo "** TX HASH :: $sTxHash **"
done

balance1=$("${DAEMON}" q bank balances "${acc1}" --node $RPC --output json)
balance1res=$(echo "${balance1}" | jq -r '.balances')
echo "** Balance of Account 1 after send_load :: $balance1res **"
balance2=$("${DAEMON}" q bank balances "${acc2}" --node $RPC --output json)
balance2res=$(echo "${balance1}" | jq -r '.balances')
echo "** Balance of Account 2 after send_load :: $balance2res **"
