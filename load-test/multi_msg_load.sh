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

if [ -z $NUM_TXS ] ; then 
	num_txs=1000
else
	num_txs=$NUM_TXS
fi

python3 $HOME/qa-integration/python-qa-tools/load-test/multi_msg_load.py $FROM $TO $num_txs