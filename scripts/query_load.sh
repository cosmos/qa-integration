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

ACC=$1
if [ -z $ACC ]
then
    ACC=1
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

acc1=$($DAEMON keys show validator$ACC -a --home $DAEMON_HOME-1 --keyring-backend test)

val1=$($DAEMON keys show validator$ACC -a --bech val --home $DAEMON_HOME-1 --keyring-backend test)

for (( a=1; a<10000; a++ ))
do

	bTx=$("${DAEMON}" q bank balances "${acc1}" --node $RPC --output json)
	
	bTxres=$(echo "${bTx}" | jq -r '.balances')
	
	echo "** Balance :: $bTxres **"
	
	sTx=$("${DAEMON}" q staking validators --node $RPC --output json)
	
	sTxres=$(echo "${sTx}" | jq -r '.validators[].description.moniker')
	
	echo "** Monikers :: $sTxres **"
	
	dTx=$("${DAEMON}" q staking delegation "${acc1}" "${val1}" --node $RPC --output json)
	
	dTxres=$(echo "${dTx}" | jq -r '.delegation.shares')
	
	echo "** Delegations :: $dTxres **"
	
done
	
	
