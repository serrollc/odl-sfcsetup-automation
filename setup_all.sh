#!/bin/bash

if [ $# -eq 0 ]; then
    echo "No arguments supplied"
    echo "USAGE: $0 <config file in json format>"
    exit
fi

if [ -z "$1" ]; then
    echo "Empty argument supplied"
    echo "USAGE: $0 <config file in json format>"
    exit
fi

if [ ! -f "$1" ]; then
    echo "Config file ($1) not found!"
    echo "USAGE: $0 <config file in json format>"
    exit
fi

#python setup_odl.py "$1"
python setup_sf.py "$1"
python setup_sff.py "$1"
python setup_server.py "$1"
python setup_client.py  "$1"
