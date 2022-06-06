#/bin/sh

## This script sends out a collection of balance queries, delegation queries
## and staking queries on the network.

set -e

# get absolute parent directory path of current file
CURPATH=`dirname $(realpath "$0")`
cd $CURPATH

# check environment variables are set
. ../deps/env-check.sh

python3 ./python-qa-tools/load-test/query_load.py $1 $2 $3 $4
