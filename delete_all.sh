#!/bin/bash

echo "deleting Service function classifiers"
python gen_delete_ServiceFunctionClassifiers.py 
echo "deleting Service function ACLs"
python gen_delete_ServiceFunctionACLs.py    
echo "deleting Service function paths"
python gen_delete_ServiceFunctionPaths.py   
echo "deleting Service function chains"
python gen_delete_ServiceFunctionChains.py  
echo "deleting Service function forwarders"
python gen_delete_ServiceFunctionsForwarders.py 
echo "deleting Service functions"
python gen_delete_ServiceFunctions.py   
echo "deleting Service nodes"
python gen_delete_ServiceNodes.py   
echo "deleting Service functions metadata"
python gen_delete_ServiceFunctionMetadata.py    


