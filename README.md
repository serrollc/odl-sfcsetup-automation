# odl-sfcsetup-automation
Python utility scripts for Opendaylight Controller(ODL) based Service Function Chain(SFC) Proof of Concept
Please refer to https://wiki.opendaylight.org/view/Service_Function_Chaining:Main for details
The scripts have been tested with Boron-SR1 release of ODL.

Utility scripts have been provided for the following

1. Install and Setup OpenDaylight controller.
2. Generate ODL controller configuration for Service Function chains(SFC)
3. Configure ODL controller for SFCs
4. Install and setup  NSH aware python Service Functions.( dummy SFs)
5. Install and setup openvswitch for Service Function Forwarder
6. Install and setup Sample client and server Nodes.

Typical SFC POC would consists of following elements

1. Overlay network consisting of set of servers hosting some services and clients accessing the same
2. One or more Service Functions like Firewall, DPI that need to be inserved in the traffic path from client to server.
3. One or more Service Function Forwarders that provide connectivity to Serivice Functions.

Preparing for building POC

1. Prepare sketch for your Test network topology (Eg Test Topology below)
2. Prepare all hosts/VMs as per your Test network topology
3. Ensure that all hosts/VMs have IP connectivity and meet below requirements
    a. Ubuntu 14.04 x86_64 LTS - trusty
    b. ssh service is enabled
    c. passwordless sudo user is set. (this user id would be used for configuring the host)
4. Get the odl-sfcsetup-automation scripts on the ODL controller Node
     git clone https://github.com/serrollc/odl-sfcsetup-automation.git
     cd odl-sfcsetup-automation
6. Prepare Configuration for your Test Topology 
    a. cp example_setup_config.json my_setup_config.json
    b. Edit my_setup_config.json for node details like IP address, username, password.
7. Prepare Configuration of ODL for your Test Topology
    a. cp example_odl_config.json my_odl_config.json
    b. Edit my_odl_config.json as per your test topology
    c. Generate ODL configuration 
       python sfc_config_util.py my_odl_config.json
       python sfc_delete_util.py my_odl_config.json

Installing and Running Services.

0. If you previously configured ODL, please clean all configuration using following script

    a. sh +x remove_config_all.sh

1. Install and enable servies in all service nodes

   a. sh +x setup_all.sh my_setup_config.json
   
      Above script will setup the ODL controller, SFF, SF, Server and Client.
      If you wish to setup each node separately, follow below steps.
      
      a. python setup_odl.py my_setup_config.json
      
      b. python setup_sf.py my_setup_config.json
      
      c. python setup_sff.py my_setup_config.json
      
      d. python setup_server.py my_setup_config.json
      
      e. python setup_client.py my_setup_config.json
      

2. Configure ODL 

    a. sh +x config_all.sh my_odl_config.json 
    
    Above script will configure all required objects in ODL. If you wish to configure
    each object separately and observe configuration in SFC UI, following below steps
    
    a. python gen_config_ServiceNode.py 
    
    b. python gen_config_ServiceFunctions.py 
    
    c. python gen_config_ServiceFunctionsForwarders.py
    
    d. python gen_config_ServiceFunctionMetadata.py
    
    e. python gen_config_ServiceFunctionChains.py
    
    f. python gen_config_ServiceFunctionPaths.py
    
    g. python gen_config_RenderedServicePath.py
    
    h. python gen_config_ServiceFunctionACLs.py
    
    i. python gen_config_ServiceFunctionClassifiers.py
    

3. Check Traffic traversing through the SFC.

   ssh to Client Node and execute below command
   
   ip netns exec app wget http://overlay_server_ip
