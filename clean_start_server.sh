#!/bin/bash

echo "$1 $2 $3"
SERVER=$1
CLIENT=$2
ODLADDR=$3

echo "Cleaning up server ..."
sudo ip netns exec app ip link set dev lo down
sudo ip netns exec app ip link set dev veth-app down
sudo ip netns exec app ifconfig veth-app down
sudo ip link set dev veth-br down
sudo ovs-vsctl del-port br-sfc veth-br
sudo ip link del veth-app
sudo ip link del veth-br
sudo ip netns del app
sudo /etc/init.d/openvswitch-switch stop
sudo rm -rf /etc/openvswitch/conf.db
echo "Configure and start ovs ..."
sudo /etc/init.d/openvswitch-switch start
sudo ovs-vsctl add-br br-sfc
sudo ovs-vsctl set-manager tcp:$ODLADDR:6640

echo "Configuring server ..."
sudo ip netns add app
sudo ip link add veth-app type veth peer name veth-br
sudo ovs-vsctl add-port br-sfc veth-br 
sudo ip link set dev veth-br up
sudo ip link set veth-app netns app
sudo ip netns exec app ifconfig veth-app $SERVER/24 up
sudo ip netns exec app ip link set dev veth-app  addr 00:00:11:11:11:11
sudo ip netns exec app arp -s $CLIENT 00:00:22:22:22:22 -i veth-app
sudo ip netns exec app ip link set dev veth-app up
sudo ip netns exec app ip link set dev lo up
sudo ip netns exec app ifconfig veth-app mtu 1400

echo "Starting http server ..."
sudo ip netns exec app python -m SimpleHTTPServer 80 > /tmp/http_server.log 2>&1  &
echo "Starting ssh server .."
sudo ip netns exec app /usr/sbin/sshd
exit 0
