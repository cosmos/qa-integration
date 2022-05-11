#/bin/sh

FROM=$1
TO=$2
python3 ../python-qa-tools/load-test/send_load.py $FROM $TO
