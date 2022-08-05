#/bin/sh

## This script tests the unit tests inside the leverage module

set -e

# get absolute parent directory path of current file
CURPATH=`dirname $(realpath "$0")`
cd $CURPATH

# check environment variables are set
. ../deps/env-check.sh

# we can pass optional arguments when running this script
# available arguments are -s/--sender, -r/--receiver, -h/--help

python3 ./internal/modules/leverage/test.py

