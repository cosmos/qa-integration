#/bin/sh

## This script generates and broadcasts 1000 transfers to and fro between two accounts.

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

python3 ./python-qa-tools/load-test/send_load.py $1 $2 $3 $4
