#/bin/sh

ACC=$1
if [ -z $ACC ]
then
    ACC=1
fi

python3 ../python-qa-tools/load-test/query_load.py $ACC
