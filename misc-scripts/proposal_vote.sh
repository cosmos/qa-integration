#/bin/sh

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

echo "--------- No.of validators who have to vote on the proposal : $NUM_VALS ------------"
IP="$(dig +short myip.opendns.com @resolver1.opendns.com)"

if [ -z $IP ]
then
    IP=127.0.0.1
fi

echo "--------Get voting period proposals--------------"
vp=$("${DAEMON}" q gov proposals --status voting_period --node $RPC --output json)
len=$(echo "${vp}" | jq -r '.proposals | length' )
echo "Length of voting period proposals : $len"
for row in $(echo "${vp}" | jq -r '.proposals | .[] | @base64'); do
  PID=$(echo "${row}" | base64 --decode | jq -r '.proposal_id')
  echo "Checking votes for proposal id : $PID"
  for (( a=1; a<=$NUM_VALS; a++ ))
  do
    DIFF=`expr $a - 1`
    INC=`expr $DIFF \* 2`
    PORT=`expr 16657 + $INC`
    RPC="http://${IP}:${PORT}"
    validator=$("${DAEMON}" keys show validator${a} --keyring-backend test --home $DAEMON_HOME-${a} --output json)
    VALADDRESS=$(echo "${validator}" | jq -r '.address')
    FROMKEY="validator${a}"
    VOTER=$VALADDRESS
    echo "voter address :: $VALADDRESS and from key :: $FROMKEY"
    getVote=$( ("${DAEMON}" q gov vote "${PID}" "${VOTER}" --node "${RPC}" --output json) 2>&1)
   
    if [ "$?" -ne 0 ]; 
    then
      #cast vote
      castVote=$( ("${DAEMON}" tx gov vote "${PID}" yes --from "${FROMKEY}" --fees 1000"${DENOM}" --chain-id "${CHAINID}" --node "${RPC}" --home $DAEMON_HOME-${a} --keyring-backend test --output json -y) 2>&1) 
      sleep 6s
      txHash=$(echo "${castVote}"| jq -r '.txhash')
      echo "TX HASH :: $txHash"
      txResult=$("${DAEMON}" q tx "${txHash}" --node $RPC --output json)
      checkVote=$(echo "${txResult}"| jq -r '.code')

      if [[ "$checkVote" != "" ]];
      then
        if [ "$checkVote" -eq 0 ];
        then
          echo "SUCCESS: $FROMKEY successfully voted on the proposal :: (proposal ID : $PID and address $VOTER ) and txHash is : $txHash"
        else 
          echo "FAILED: $FROMKEY getting error while casting vote for ( Proposl ID : $PID and address $VOTER ) and txHash is : $txhash and REASON : $(echo "${castVote}" | jq '.raw_log')"
        fi
      fi
    else
      voted=$(echo "${getVote}" | jq -r '.option')
      echo "Already casted vote: $voted on proposal ID : $PID from $FROMKEY address : $VOTER"
    fi
  done
done
