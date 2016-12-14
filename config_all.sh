#!/bin/bash


python gen_config_ServiceNode.py 
python gen_config_ServiceFunctions.py 
python gen_config_ServiceFunctionsForwarders.py 
python gen_config_ServiceFunctionMetadata.py    
python gen_config_ServiceFunctionChains.py  
python gen_config_ServiceFunctionPaths.py   
python gen_config_RenderedServicePath.py    
python gen_config_ServiceFunctionACLs.py    
python gen_config_ServiceFunctionClassifiers.py 

