#/bin/sh

set -e

# get absolute parent directory path of current file
CURPATH=`dirname $(realpath "$0")`
cd $CURPATH

# check environment variables are set
. ../deps/env-check.sh

python3 ./python-qa-tools/load-test/single_msg_load.py $1 $2 $3 $4 $5 $6
