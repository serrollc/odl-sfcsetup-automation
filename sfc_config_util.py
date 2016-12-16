#!/usr/bin/python
import argparse
import requests,json
from requests.auth import HTTPBasicAuth
from subprocess import call
import time
import sys
import os
from pprint import pprint

#```````````````````````````````````````````
#Global data
gInput      = ""
#,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

#--------------------------------------------------------------------------
# function copied from boron/sfc-demo/sfc103/setup_sfc.py and modified
#--------------------------------------------------------------------------

def get_service_nodes_uri():
    return "/restconf/config/service-node:service-nodes"

def get_service_nodes_data():
    global gInput  
    sns = { "service-nodes": { "service-node": [ { "name": node['name'], "ip-mgmt-address": node['ip-address'] } for node in gInput['service-nodes'] ] } } 

    #jsns = json.dumps(sns, indent=4)
    #print jsns
    return sns
        
def get_service_functions_uri():
    return "/restconf/config/service-function:service-functions"

def get_service_functions_data():
    global gInput 

    sfs  = {"service-functions": { "service-function": [ { "name":node['name'], "ip-mgmt-address":node['ip-address'], "rest-uri":"http://"+node['ip-address']+":5000",  "type":node['type'], "nsh-aware": "true", "sf-data-plane-locator": { "name":node['name']+"-dpl", "port": 6633, "ip":node['ip-address'],"transport": "service-locator:vxlan-gpe", "service-function-forwarder": node['sff_name'] } } for node in gInput['service-functions'] ] } }
    #jsfs = json.dumps(sfs, indent=4)
    #print jsfs
    return sfs

def get_service_function_forwarders_uri():
    return "/restconf/config/service-function-forwarder:service-function-forwarders"

def get_service_function_forwarders_data():
    global gInput 

    #sffs    = { "service-function-forwarders": { "service-function-forwarder": [ {"name":node['name'],"service-node":node['service_node'], "service-function-forwarder-ovs:ovs-bridge": { "bridge-name": "br-sfc" } }  for node in gInput['service-function-forwarders'] ] } }
    sffs = {}
    sffs["service-function-forwarders"] = {}
    sffs["service-function-forwarders"]["service-function-forwarder"] = list()

    for node in gInput['service-function-forwarders']:
        counter = 1 
        sff_dp_locator = list()
        sf_dictionary  = list()
        if len(node['service_function']) > 0:
            for ele in node['service_function']:
                sff_dp_locator.append({"name":node['name']+"-"+str(counter)+"-dpl", "data-plane-locator": { "transport": "service-locator:vxlan-gpe", "port": 6633, "ip":node['ip-address']}, "service-function-forwarder-ovs:ovs-options": { "remote-ip": "flow", "dst-port": "6633", "key": "flow", "nsp": "flow", "nsi": "flow", "nshc1": "flow", "nshc2": "flow", "nshc3": "flow", "nshc4": "flow", "exts":"gpe" } })
                sf_dictionary.append( { "name": ele, "sff-sf-data-plane-locator": { "sf-dpl-name": ele+"-dpl", "sff-dpl-name": node['name']+"-"+str(counter)+"-dpl" } })
                counter+=1
        else:
            sff_dp_locator.append({"name":node['name']+"-"+str(counter)+"-dpl", "data-plane-locator": { "transport": "service-locator:vxlan-gpe", "port": 6633, "ip":node['ip-address']}, "service-function-forwarder-ovs:ovs-options": { "remote-ip": "flow", "dst-port": "6633", "key": "flow", "nsp": "flow", "nsi": "flow", "nshc1": "flow", "nshc2": "flow", "nshc3": "flow", "nshc4": "flow", "exts":"gpe" } }) 

        if counter > 1:
            sffs["service-function-forwarders"]["service-function-forwarder"].append({ "name":node['name'],"service-node":node['service_node'], "service-function-forwarder-ovs:ovs-bridge": { "bridge-name": "br-sfc" }, "sff-data-plane-locator":sff_dp_locator, "service-function-dictionary":sf_dictionary })
        else: 
            sffs["service-function-forwarders"]["service-function-forwarder"].append({ "name":node['name'],"service-node":node['service_node'], "service-function-forwarder-ovs:ovs-bridge": { "bridge-name": "br-sfc" }, "sff-data-plane-locator":sff_dp_locator})

    
    #jsffs = json.dumps(sffs, indent=4)
    #print jsffs
    return sffs


def get_service_function_chains_uri():
    return "/restconf/config/service-function-chain:service-function-chains/"

def get_service_function_chains_data():
    global gInput    
    #sfcs = { "service-function-chains": { "service-function-chain": [ { "name": node['name'], "symmetric":node['symmetric'], "sfc-service-function": [{"name":ele, "type":"dpi"} for ele in node['service_function'] ] } for node in gInput['service-function-chains'] ] } } 
    sfcs = {}
    sfcs["service-function-chains"] = {}
    sfcs["service-function-chains"]["service-function-chain"] = list()

    for node in gInput['service-function-chains']:
        sfc_sf = list()
        for ele in node['service_function']:
            for sf in gInput['service-functions']:
                if sf['name'] == ele:
                    sf_type = sf['type']
            sfc_sf.append({"name":ele, "type":sf_type})


        sfcs["service-function-chains"]["service-function-chain"].append({ "name": node['name'], "symmetric":node['symmetric'], "sfc-service-function": sfc_sf })


    #jsfcs = json.dumps(sfcs, indent=4)
    #print jsfcs
    return sfcs

def get_service_function_paths_uri():
    return "/restconf/config/service-function-path:service-function-paths/"

def get_service_function_paths_data():
    global gInput 
    sfps = {}
    sfps["service-function-paths"] = {}
    sfps["service-function-paths"]["service-function-path"] = list()
     
    for node in gInput['service-function-chains']:
        sfps["service-function-paths"]["service-function-path"].append( {"name":node['name']+"-"+"SFP", "service-chain-name":node['name'],"starting-index": 255, "symmetric":node['symmetric'],"context-metadata": "NSH1" })

    #jsfps = json.dumps(sfps, indent=4)
    #print jsfps
    return sfps   

def get_service_function_metadata_uri():
    return "/restconf/config/service-function-path-metadata:service-function-metadata/"

def get_service_function_metadata_data():
    return  {
            "service-function-metadata": {
                "context-metadata": [
                {
                "name": "NSH1",
                "context-header1": "1",
                "context-header2": "2",
                "context-header3": "3",
                "context-header4": "4"
                }
            ]
        }
    }

def get_rendered_service_path_uri():
    return "/restconf/operations/rendered-service-path:create-rendered-path/"

def get_rendered_service_path_data():
    global gInput  
    rsps = { "input": [ { "name":"RSP-"+node['name'], "parent-service-function-path": node['name']+"-"+"SFP", "symmetric":node['symmetric'] } for node in gInput['service-function-chains'] ] } 

    #jrsps = json.dumps(rsps, indent=4)
    #print jrsps
    return rsps
 
def get_service_function_acl_uri():
    return "/restconf/config/ietf-access-control-list:access-lists/"

def get_service_function_acl_data():
    global gInput
    acls = {}

    acl_list = list()
    for node in gInput['acls']:
        ace_list = list()
        for ace in node['aces']:
            matches = {"destination-ipv4-network": ace['diprange'], "source-ipv4-network": ace['siprange'], "protocol": ace['proto'], "source-port-range": { "lower-port": ace['sprange'][0], "upper-port": ace['sprange'][1] }, "destination-port-range": { "lower-port": ace['dprange'][0], "upper-port": ace['dprange'][1] }}
            fwd = "Forward"
            if ace['direction'].lower() == fwd.lower():
                ace_list.append({"rule-name":ace['name'], "actions": { "service-function-acl:rendered-service-path": "RSP-"+ace['action']}, "matches": matches })
            else:
                ace_list.append({"rule-name":ace['name'], "actions": { "service-function-acl:rendered-service-path": "RSP-"+ace['action']+"-Reverse"}, "matches": matches })

    
        acl_list.append({"acl-name":node['name'], "acl-type": "ietf-access-control-list:ipv4-acl", "access-list-entries": {"ace": ace_list}})

    acls['access-lists'] = {"acl":acl_list}
    #acls['access-lists'].append({"acl":acl_list})
    
    #jacls = json.dumps(acls, indent=4)
    #print jacls
    return acls

def get_service_function_classifiers_uri():
    return "/restconf/config/service-function-classifier:service-function-classifiers/"

def get_service_function_classifiers_data():
    global gInput 


    sfcls = { "service-function-classifiers": { "service-function-classifier": [ { "name": node['name'], "scl-service-function-forwarder":[{"name": node['sff'], "interface": node['interface']}], "acl": {"name": node['acl'], "type": "ietf-access-control-list:ipv4-acl" } } for node in gInput['service-function-classifiers'] ] } } 

    #jsfcls = json.dumps(sfcls, indent=4)
    #print jsfcls
    return sfcls


#--------------------------------------------------------------------------


def test_print():
    pprint(data)
    print "================================================"
    print data['odl-configuration']['controller']['name']
    print data['odl-configuration']['controller']['ip-address']
    print "================================================"
    print data['odl-configuration']['service-functions']
    print "================================================"
    print data['odl-configuration']['service-function-forwarders']
    print "================================================"
    print data['odl-configuration']['service-function-forwarders'][1]['ip-address']

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
outfilename   = exec_dirname + "/gen_config_ServiceNode.py"
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
    op_fp.write("rest_utils.put(controller_ip, controller_port, controller_user, controller_pass, config_uri, config_data)\n\n")
    op_fp.flush()


#create file for Service Functions configuration
outfilename   = exec_dirname + "/gen_config_ServiceFunctions.py"
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
    op_fp.write("rest_utils.put(controller_ip, controller_port, controller_user, controller_pass, config_uri, config_data)\n\n")
    op_fp.flush()


#create file for Service Function Forwarders configuration
outfilename   = exec_dirname + "/gen_config_ServiceFunctionsForwarders.py"
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
    op_fp.write("rest_utils.put(controller_ip, controller_port, controller_user, controller_pass, config_uri, config_data)\n\n")
    op_fp.flush()


#create file for Service Function Chains configuration
outfilename   = exec_dirname + "/gen_config_ServiceFunctionChains.py"
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
    op_fp.write("rest_utils.put(controller_ip, controller_port, controller_user, controller_pass, config_uri, config_data)\n\n")
    op_fp.flush()

#create file for Service Function Metadata configuration
outfilename   = exec_dirname + "/gen_config_ServiceFunctionMetadata.py"
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
    op_fp.write("rest_utils.put(controller_ip, controller_port, controller_user, controller_pass, config_uri, config_data)\n\n")
    op_fp.flush()

#create file for Service Function Paths configuration
outfilename   = exec_dirname + "/gen_config_ServiceFunctionPaths.py"
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
    op_fp.write("rest_utils.put(controller_ip, controller_port, controller_user, controller_pass, config_uri, config_data)\n\n")
    op_fp.flush()


#create file for Render Service Paths configuration
outfilename   = exec_dirname + "/gen_config_RenderedServicePath.py"
with open(outfilename, 'w') as op_fp:
    op_fp.write("import requests,json\n")
    op_fp.write("from requests.auth import HTTPBasicAuth\n")
    op_fp.write("import rest_utils\n")
    op_fp.write("\n\n\n")
    op_fp.write("controller_ip    = \""+ gInput['controller']['ip-address'] + "\"\n")
    op_fp.write("controller_port  = \""+ gInput['controller']['port'] + "\"\n")
    op_fp.write("controller_user  = \""+ gInput['controller']['user'] + "\"\n")
    op_fp.write("controller_pass  = \""+ gInput['controller']['password'] + "\"\n")
    op_fp.write("config_uri       = \"" +get_rendered_service_path_uri()+ "\"\n\n\n")
    loopVar=1
    for node in gInput['service-function-chains']:
        rsps = { "input": { "name":"RSP-"+node['name'], "parent-service-function-path":node['name']+"-"+"SFP", "symmetric":node['symmetric'] } }
        op_fp.write("config_data"+str(loopVar) + "      = " + json.dumps(rsps,indent=4) + "\n")
        op_fp.write("rest_utils.post(controller_ip, controller_port, controller_user, controller_pass, config_uri, config_data"+str(loopVar)+")\n\n")
        loopVar+=1

    op_fp.flush()


#create file for Service Function ACLs configuration
outfilename   = exec_dirname + "/gen_config_ServiceFunctionACLs.py"
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
    op_fp.write("rest_utils.put(controller_ip, controller_port, controller_user, controller_pass, config_uri, config_data)\n\n")
    op_fp.flush()


#create file for Service Function Classifiers configuration
outfilename   = exec_dirname + "/gen_config_ServiceFunctionClassifiers.py"
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
    op_fp.write("rest_utils.put(controller_ip, controller_port, controller_user, controller_pass, config_uri, config_data)\n\n")
    op_fp.flush()



