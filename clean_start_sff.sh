#!/bin/bash

echo "$1"

echo "Cleaning up OVS ..."
sudo /etc/init.d/openvswitch-switch stop
sudo rm -rf /etc/openvswitch/conf.db

echo "Configure and start ovs ..."
sudo /etc/init.d/openvswitch-switch start
sudo ovs-vsctl add-br br-sfc
sudo ovs-vsctl set-manager tcp:$1:6640


