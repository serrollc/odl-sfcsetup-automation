#!/bin/bash

echo "configuring Service node ..."
python gen_config_ServiceNode.py 
echo "configuring Service functions ..."
python gen_config_ServiceFunctions.py 
echo "configuring Service functions forwarders ..."
python gen_config_ServiceFunctionsForwarders.py 
echo "configuring Service functions metadata ..."
python gen_config_ServiceFunctionMetadata.py    
echo "configuring Service functions chains ..."
python gen_config_ServiceFunctionChains.py  
echo "configuring Service functions paths ..."
python gen_config_ServiceFunctionPaths.py   
echo "configuring Render service path ..."
python gen_config_RenderedServicePath.py    
echo "configuring Service functions ACLs ..."
python gen_config_ServiceFunctionACLs.py    
echo "configuring Service functions classifiers ..."
python gen_config_ServiceFunctionClassifiers.py 

