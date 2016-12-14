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

python delete_ServiceFunctionClassifiers.py "$1"
python delete_ServiceFunctionACLs.py    "$1"
python delete_RenderedServicePath.py "$1"
python delete_ServiceFunctionChains.py  "$1"
python delete_ServiceFunctionPaths.py   "$1"
python delete_ServiceFunctionsForwarders.py "$1"
python delete_ServiceFunctions.py   "$1"
python delete_ServiceNodes.py   "$1"
python delete_ServiceFunctionMetadata.py    "$1"


