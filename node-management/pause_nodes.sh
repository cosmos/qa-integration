#/bin/sh

## This script pauses the systemd process of the nodes.

NODES=$1
if [ -z $NODES ]
then
    NODES=1
fi

echo "**** Number of nodes to be paused: $NODES ****"
echo "---------- Stopping systemd service files --------"
for (( a=1; a<=$NODES; a++ ))
do
    sudo -S systemctl stop $DAEMON-${a}.service
    echo "-- Stopped $DAEMON-${a}.service --"
done
