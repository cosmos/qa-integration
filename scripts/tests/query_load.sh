#/bin/sh

## This script sends out a collection of balance queries, delegation queries
## and staking queries on the network.

set -e

# get absolute parent directory path of current file
CURPATH=`dirname $(realpath "$0")`
cd $CURPATH

# check environment variables are set
. ../deps/env-check.sh

# we can pass optional arguments when running this script
# available arguments are -s/--sender, -h/--help
# example: ./query_load.sh -s cosmos1f2838advrjl3c8h4kjfvfmhkh0gs0wf6cyzwu8
# python3 ./internal/load-test/query_load.py $1 $2
docker exec -e PYTHONPATH=/:/internal --env-file ./env  -it $CONTAINER_NAME sh -c "python3 /internal/load-test/query_load.py"
