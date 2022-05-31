#/bin/sh

## This script stops the systemd process of the nodes and removes their data directories.

NODES=$1
if [ -z $NODES ]
then
    NODES=1
fi

echo "**** Number of nodes to be shutdown and disabled: $NODES ****"
echo "---------- Stopping systemd service files --------"
for (( a=1; a<=$NODES; a++ ))
do
    sudo -S systemctl stop $DAEMON-${a}.service
    echo "-- Stopped $DAEMON-${a}.service --"
done
echo "------- Running unsafe reset all ---------"
for (( a=1; a<=$NODES; a++ ))
do
    $DAEMON unsafe-reset-all  --home $DAEMON_HOME-$a    
    rm -rf $DAEMON_HOME-$a
    echo "-- Executed $DAEMON unsafe-reset-all  --home $DAEMON_HOME-$a --"
done
echo "---------- Disabling systemd process files --------"
for (( a=1; a<=$NODES; a++ ))
do
   sudo -S systemctl disable $DAEMON-${a}.service
   echo "-- Executed sudo -S systemctl disable $DAEMON-${a}.service --"
done
