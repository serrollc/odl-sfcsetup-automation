#!/usr/bin/python
import argparse
import requests,json
from requests.auth import HTTPBasicAuth
from subprocess import call
import time
import sys
import os
from pprint import pprint
def get_service_nodes_uri():
    return "/restconf/config/service-node:service-nodes"

def get_service_nodes_data():
    global gInput  
    sns = { "service-nodes": "delete" } 
    return sns
        
def get_service_functions_uri():
    return "/restconf/config/service-function:service-functions"

def get_service_functions_data():
    global gInput 
    sfs  = {"service-functions": "delete" }
    return sfs

def get_service_function_forwarders_uri():
    return "/restconf/config/service-function-forwarder:service-function-forwarders"

def get_service_function_forwarders_data():
    global gInput 
    sffs    = { "service-function-forwarders": "delete" }
    return sffs


def get_service_function_chains_uri():
    return "/restconf/config/service-function-chain:service-function-chains/"

def get_service_function_chains_data():
    global gInput    
    sfcs = { "service-function-chains": "delete" } 
    return sfcs

def get_service_function_paths_uri():
    return "/restconf/config/service-function-path:service-function-paths/"

def get_service_function_paths_data():
    global gInput 
    sfps = { "service-function-paths" : "delete" }
    return sfps   

def get_service_function_metadata_uri():
    return "/restconf/config/service-function-path-metadata:service-function-metadata/"

def get_service_function_metadata_data():
    return  {
            "service-function-metadata": "delete" 
    }

def get_rendered_service_path_uri():
    return "/restconf/operations/rendered-service-path:delete-rendered-path/"
        

def get_rendered_service_path_data():
    global gInput  
    rsps = { "input": "delete" } 
    return rsps
 
def get_service_function_acl_uri():
    return "/restconf/config/ietf-access-control-list:access-lists/"

def get_service_function_acl_data():
    global gInput
    acls = {"access-lists":"delete"}
    return acls

def get_service_function_classifiers_uri():
    return "/restconf/config/service-function-classifier:service-function-classifiers/"

def get_service_function_classifiers_data():
    global gInput 
    sfcls = { "service-function-classifiers": "delete"}
    return sfcls


#--------------------------------------------------------------------------

def validate_and_load_input(input_file):
    global gInput
    try:
        with open(input_file) as data_fp:    
            gInput = json.load(data_fp)
            #print gInput
    except ValueError, e:
        print "Fix following error in input JSON file=" + input_file + "."
        print e
        print
        return False

    return True


#=======================================================================================
if len(sys.argv) < 2 :
    print ""
    print "Usage: " + sys.argv[0] + "<full path to file containing config in JSON format>"
    exit(0)

#check if input file exists
if not os.path.exists(sys.argv[1]):
    print ""
    print "Configuration files or path does not exists - " + sys.argv[1]
    print ""
    print "Usage: " + sys.argv[0] + " <full path to file containing config in JSON format>"
    exit(0)

#check if input file data correctness
return_code = validate_and_load_input(sys.argv[1])
if return_code == False :
    print "____________________________________________"
else:
    print "Generating configuration..."
    #print gInput['odl-configuration']['service-function-forwarders'][1]['ip-address']

#create outpur file name as script_folder + output.py
exec_dirname  = os.path.dirname(os.path.realpath(sys.argv[0]))
#create file for Service Node configuration
outfilename   = exec_dirname + "/gen_delete_ServiceNodes.py"
with open(outfilename, 'w') as op_fp:
    op_fp.write("import requests,json\n")
    op_fp.write("from requests.auth import HTTPBasicAuth\n")
    op_fp.write("import rest_utils\n")
    op_fp.write("\n\n\n")
    op_fp.write("controller_ip    = \""+ gInput['controller']['ip-address'] + "\"\n")
    op_fp.write("controller_port  = \""+ gInput['controller']['port'] + "\"\n")
    op_fp.write("controller_user  = \""+ gInput['controller']['user'] + "\"\n")
    op_fp.write("controller_pass  = \""+ gInput['controller']['password'] + "\"\n")
    op_fp.write("config_uri       = \"" +get_service_nodes_uri()+ "\"\n")
    op_fp.write("config_data      = " + json.dumps(get_service_nodes_data(),indent=4)+"\n\n\n")
    op_fp.write("rest_utils.delete(controller_ip, controller_port, controller_user, controller_pass, config_uri, config_data)\n\n")
    op_fp.flush()


#create file for Service Functions configuration
outfilename   = exec_dirname + "/gen_delete_ServiceFunctions.py"
with open(outfilename, 'w') as op_fp:
    op_fp.write("import requests,json\n")
    op_fp.write("from requests.auth import HTTPBasicAuth\n")
    op_fp.write("import rest_utils\n")
    op_fp.write("\n\n\n")
    op_fp.write("controller_ip    = \""+ gInput['controller']['ip-address'] + "\"\n")
    op_fp.write("controller_port  = \""+ gInput['controller']['port'] + "\"\n")
    op_fp.write("controller_user  = \""+ gInput['controller']['user'] + "\"\n")
    op_fp.write("controller_pass  = \""+ gInput['controller']['password'] + "\"\n")
    op_fp.write("config_uri       = \"" +get_service_functions_uri()+ "\"\n")
    op_fp.write("config_data      = " + json.dumps(get_service_functions_data(),indent=4)+"\n\n\n")
    op_fp.write("rest_utils.delete(controller_ip, controller_port, controller_user, controller_pass, config_uri, config_data)\n\n")
    op_fp.flush()


#create file for Service Function Forwarders configuration
outfilename   = exec_dirname + "/gen_delete_ServiceFunctionsForwarders.py"
with open(outfilename, 'w') as op_fp:
    op_fp.write("import requests,json\n")
    op_fp.write("from requests.auth import HTTPBasicAuth\n")
    op_fp.write("import rest_utils\n")
    op_fp.write("\n\n\n")
    op_fp.write("controller_ip    = \""+ gInput['controller']['ip-address'] + "\"\n")
    op_fp.write("controller_port  = \""+ gInput['controller']['port'] + "\"\n")
    op_fp.write("controller_user  = \""+ gInput['controller']['user'] + "\"\n")
    op_fp.write("controller_pass  = \""+ gInput['controller']['password'] + "\"\n")
    op_fp.write("config_uri       = \"" +get_service_function_forwarders_uri()+ "\"\n")
    op_fp.write("config_data      = " + json.dumps(get_service_function_forwarders_data(),indent=4)+"\n\n\n")
    op_fp.write("rest_utils.delete(controller_ip, controller_port, controller_user, controller_pass, config_uri, config_data)\n\n")
    op_fp.flush()


#create file for Service Function Chains configuration
outfilename   = exec_dirname + "/gen_delete_ServiceFunctionChains.py"
with open(outfilename, 'w') as op_fp:
    op_fp.write("import requests,json\n")
    op_fp.write("from requests.auth import HTTPBasicAuth\n")
    op_fp.write("import rest_utils\n")
    op_fp.write("\n\n\n")
    op_fp.write("controller_ip    = \""+ gInput['controller']['ip-address'] + "\"\n")
    op_fp.write("controller_port  = \""+ gInput['controller']['port'] + "\"\n")
    op_fp.write("controller_user  = \""+ gInput['controller']['user'] + "\"\n")
    op_fp.write("controller_pass  = \""+ gInput['controller']['password'] + "\"\n")
    op_fp.write("config_uri       = \"" +get_service_function_chains_uri()+ "\"\n")
    op_fp.write("config_data      = " + json.dumps(get_service_function_chains_data(),indent=4)+"\n\n\n")
    op_fp.write("rest_utils.delete(controller_ip, controller_port, controller_user, controller_pass, config_uri, config_data)\n\n")
    op_fp.flush()

#create file for Service Function Metadata configuration
outfilename   = exec_dirname + "/gen_delete_ServiceFunctionMetadata.py"
with open(outfilename, 'w') as op_fp:
    op_fp.write("import requests,json\n")
    op_fp.write("from requests.auth import HTTPBasicAuth\n")
    op_fp.write("import rest_utils\n")
    op_fp.write("\n\n\n")
    op_fp.write("controller_ip    = \""+ gInput['controller']['ip-address'] + "\"\n")
    op_fp.write("controller_port  = \""+ gInput['controller']['port'] + "\"\n")
    op_fp.write("controller_user  = \""+ gInput['controller']['user'] + "\"\n")
    op_fp.write("controller_pass  = \""+ gInput['controller']['password'] + "\"\n")
    op_fp.write("config_uri       = \"" +get_service_function_metadata_uri()+ "\"\n")
    op_fp.write("config_data      = " + json.dumps(get_service_function_metadata_data(),indent=4)+"\n\n\n")
    op_fp.write("rest_utils.delete(controller_ip, controller_port, controller_user, controller_pass, config_uri, config_data)\n\n")
    op_fp.flush()

#create file for Service Function Paths configuration
outfilename   = exec_dirname + "/gen_delete_ServiceFunctionPaths.py"
with open(outfilename, 'w') as op_fp:
    op_fp.write("import requests,json\n")
    op_fp.write("from requests.auth import HTTPBasicAuth\n")
    op_fp.write("import rest_utils\n")
    op_fp.write("\n\n\n")
    op_fp.write("controller_ip    = \""+ gInput['controller']['ip-address'] + "\"\n")
    op_fp.write("controller_port  = \""+ gInput['controller']['port'] + "\"\n")
    op_fp.write("controller_user  = \""+ gInput['controller']['user'] + "\"\n")
    op_fp.write("controller_pass  = \""+ gInput['controller']['password'] + "\"\n")
    op_fp.write("config_uri       = \"" +get_service_function_paths_uri()+ "\"\n")
    op_fp.write("config_data      = " + json.dumps(get_service_function_paths_data(),indent=4)+"\n\n\n")
    op_fp.write("rest_utils.delete(controller_ip, controller_port, controller_user, controller_pass, config_uri, config_data)\n\n")
    op_fp.flush()

'''
#create file for Render Service Paths configuration
outfilename   = exec_dirname + "/gen_delete_RenderedServicePath.py"
with open(outfilename, 'w') as op_fp:
    op_fp.write("import requests,json\n")
    op_fp.write("from requests.auth import HTTPBasicAuth\n")
    op_fp.write("import rest_utils\n")
    op_fp.write("\n\n\n")
    op_fp.write("controller_ip    = \""+ gInput['controller']['ip-address'] + "\"\n")
    op_fp.write("controller_port  = \""+ gInput['controller']['port'] + "\"\n")
    op_fp.write("controller_user  = \""+ gInput['controller']['user'] + "\"\n")
    op_fp.write("controller_pass  = \""+ gInput['controller']['password'] + "\"\n")
    op_fp.write("config_uri       = \"" +get_rendered_service_path_uri()+ "\"\n")
    #XXX TODO - Write loop for each sfcs create rsp with new viriable
    op_fp.write("config_data      = " + json.dumps(get_rendered_service_path_data(),indent=4)+"\n\n\n")
    op_fp.write("rest_utils.delete(controller_ip, controller_port, controller_user, controller_pass, config_uri, config_data)\n\n")
    op_fp.flush()
'''

#create file for Service Function ACLs configuration
outfilename   = exec_dirname + "/gen_delete_ServiceFunctionACLs.py"
with open(outfilename, 'w') as op_fp:
    op_fp.write("import requests,json\n")
    op_fp.write("from requests.auth import HTTPBasicAuth\n")
    op_fp.write("import rest_utils\n")
    op_fp.write("\n\n\n")
    op_fp.write("controller_ip    = \""+ gInput['controller']['ip-address'] + "\"\n")
    op_fp.write("controller_port  = \""+ gInput['controller']['port'] + "\"\n")
    op_fp.write("controller_user  = \""+ gInput['controller']['user'] + "\"\n")
    op_fp.write("controller_pass  = \""+ gInput['controller']['password'] + "\"\n")
    op_fp.write("config_uri       = \"" +get_service_function_acl_uri()+ "\"\n")
    op_fp.write("config_data      = " + json.dumps(get_service_function_acl_data(),indent=4)+"\n\n\n")
    op_fp.write("rest_utils.delete(controller_ip, controller_port, controller_user, controller_pass, config_uri, config_data)\n\n")
    op_fp.flush()


#create file for Service Function Classifiers configuration
outfilename   = exec_dirname + "/gen_delete_ServiceFunctionClassifiers.py"
with open(outfilename, 'w') as op_fp:
    op_fp.write("import requests,json\n")
    op_fp.write("from requests.auth import HTTPBasicAuth\n")
    op_fp.write("import rest_utils\n")
    op_fp.write("\n\n\n")
    op_fp.write("controller_ip    = \""+ gInput['controller']['ip-address'] + "\"\n")
    op_fp.write("controller_port  = \""+ gInput['controller']['port'] + "\"\n")
    op_fp.write("controller_user  = \""+ gInput['controller']['user'] + "\"\n")
    op_fp.write("controller_pass  = \""+ gInput['controller']['password'] + "\"\n")
    op_fp.write("config_uri       = \"" +get_service_function_classifiers_uri()+ "\"\n")
    op_fp.write("config_data      = " + json.dumps(get_service_function_classifiers_data(),indent=4)+"\n\n\n")
    op_fp.write("rest_utils.delete(controller_ip, controller_port, controller_user, controller_pass, config_uri, config_data)\n\n")
    op_fp.flush()



