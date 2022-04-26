#/bin/sh

FROM=$1
if [ -z $FROM ]
then
    FROM=1
fi

TO=$2
if [ -z $TO ]
then
    TO=2
fi

python3 ../python-qa-tools/load-test/send_load.py $FROM $TO
