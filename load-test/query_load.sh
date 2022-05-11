#/bin/sh

ACC=$1
NUM_TXS=$2
python3 ../python-qa-tools/load-test/query_load.py $ACC $NUM_TXS
