#/bin/sh

FROM=$1

TO=$2

NUM_TXS=$3

python3 $HOME/qa-integration/python-qa-tools/load-test/single_msg_load.py $FROM $TO $NUM_TXS
