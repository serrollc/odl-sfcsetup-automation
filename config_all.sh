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

python config_ServiceNode.py "$1"
python config_ServiceFunctions.py "$1"
python config_ServiceFunctionsForwarders.py "$1"
python config_ServiceFunctionPaths.py   "$1"
python config_ServiceFunctionMetadata.py    "$1"
python config_ServiceFunctionChains.py  "$1"
python config_RenderedServicePath.py    "$1"
python config_ServiceFunctionACLs.py    "$1"
python config_ServiceFunctionClassifiers.py "$1"

