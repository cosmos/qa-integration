#/bin/sh

## This script restarts the systemd process of the nodes. 

NODES=$1
if [ -z $NODES ]
then
    NODES=1
fi

echo "**** Number of nodes to be resumed: $NODES ****"
echo "---------- Restarting systemd service files --------"
for (( a=1; a<=$NODES; a++ ))
do
    sudo -S systemctl restart $DAEMON-${a}.service
    echo "-- Resumed $DAEMON-${a}.service --"
done
