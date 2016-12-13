#!/bin/bash

echo "$1 $2 $3"

echo "Cleaning up client ..."
sudo ip netns exec app ip link set dev lo down
sudo ip netns exec app ip link set dev veth-app down
sudo ip netns exec app ifconfig veth-app down
sudo ip link set dev veth-br down
sudo ovs-vsctl del-port br-sfc veth-br
sudo ip link del veth-app
sudo ip netns del app
sudo /etc/init.d/openvswitch-switch stop
sudo rm -rf /etc/openvswitch/conf.db
echo "Configure and start ovs ..."
sudo /etc/init.d/openvswitch-switch start
sudo ovs-vsctl add-br br-sfc
sudo ovs-vsctl set-manager tcp:$3:6640
echo "Configuring client ..."
sudo ip netns add app
sudo ip link add veth-app type veth peer name veth-br
sudo ovs-vsctl add-port br-sfc veth-br 
sudo ip link set dev veth-br up
sudo ip link set veth-app netns app
sudo ip netns exec app ifconfig veth-app $2/24 up
sudo ip netns exec app ip link set dev veth-app  addr 00:00:11:11:11:11
sudo ip netns exec app arp -s $1 00:00:22:22:22:22 -i veth-app
sudo ip netns exec app ip link set dev veth-app up
sudo ip netns exec app ip link set dev lo up
sudo ip netns exec app ifconfig veth-app mtu 1400
exit 0
