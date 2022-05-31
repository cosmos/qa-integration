#/bin/sh
set -e

# get absolute parent directory path of current file
CURPATH=`dirname $(realpath "$0")`
cd $CURPATH

# set pythonpath environment
cd ..
export PYTHONPATH=$PWD:$PWD/python-qa-tools
echo $PYTHONPATH

# check environment variables are set
bash ./deps/env-check.sh $CURPATH

python3 ./python-qa-tools/load-test/multi_msg_load.py $1 $2 $3 $4 $5 $6
