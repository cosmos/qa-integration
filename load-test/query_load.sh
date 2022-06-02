#/bin/sh

## This script sends out a collection of balance queries, delegation queries
## and staking queries on the network.

set -e

# get absolute parent directory path of current file
CURPATH=`dirname $(realpath "$0")`
cd $CURPATH

# set environment with env config.
set -a
source ../env
set +a

# set pythonpath environment
cd ..
export PYTHONPATH=$PWD:$PWD/python-qa-tools
echo $PYTHONPATH

# check environment variables are set
bash ./deps/env-check.sh $CURPATH

python3 ./python-qa-tools/load-test/query_load.py $1 $2 $3 $4
