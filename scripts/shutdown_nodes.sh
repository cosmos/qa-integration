#/bin/sh

NODES=$1
if [ -z $NODES ]
then
    NODES=1
fi

echo "**** Number of nodes to be shutdown: $NODES ****"

echo "---------- Stopping systemd service files --------"

for (( a=1; a<=$NODES; a++ ))
do
    sudo -S systemctl stop $DAEMON-${a}.service

    echo "-- Executed sudo -S systemctl stop $DAEMON-${a}.service --"
done

echo

echo "------- Running unsafe reset all ---------"

for (( a=1; a<=$NODES; a++ ))
do
    $DAEMON unsafe-reset-all  --home $DAEMON_HOME-$a
    
    rm -rf $DAEMON_HOME-$a

    echo "-- Executed $DAEMON unsafe-reset-all  --home $DAEMON_HOME-$a --"
done

echo

echo "---------- Disabling systemd process files --------"

for (( a=1; a<=$NODES; a++ ))
do
   sudo -S systemctl disable $DAEMON-${a}.service

   echo "-- Executed sudo -S systemctl disable $DAEMON-${a}.service --"
done

echo