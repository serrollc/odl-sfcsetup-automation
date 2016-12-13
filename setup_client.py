#!/usr/bin/python
import requests,json
import sys, os, re
from pprint import pprint
#import paramiko
import traceback, logging
import ssh_apis

#Global data
gUserInputData      = ""
gOvsSetupFile       = "clean_install_ovs.sh" 
gClientSetupFile    = "clean_start_client.sh" 


def validate_and_load_input(input_file):
    global gUserInputData
    try:
        with open(input_file) as data_fp:
            gUserInputData = json.load(data_fp)
            #print gUserInputData
    except ValueError, e:
        print "Fix following error in input JSON file=" + input_file + "."
        print e
        print
        return False

    return True

 
#=======================================================================================
#****************************************************

gLogFd =  logging.getLogger(__name__)
#****************************************************

if len(sys.argv) < 2 :
    print ""
    print "Usage: " + sys.argv[0] + "<full path to file containing host config in JSON format>"
    exit(0)

#check if input file exists
if not os.path.exists(sys.argv[1]):
    print ""
    print "Configuration files or path does not exists - " + sys.argv[1]
    print ""
    print "Usage: " + sys.argv[0] + " <input file in JSON format>"
    exit(0)


#check if input file data correctness
return_code = validate_and_load_input(sys.argv[1])
if return_code == False :
    print "____________________________________________"
else:
    print "Generating setup files ..."
    #print gUserInputData['odl-configuration']['service-function-forwarders'][1]['ip-address']

#create outpur file name as script_folder + output.py
exec_dirname  = os.path.dirname(os.path.realpath(sys.argv[0]))


#create file for Service Node configuration
ovsFilename   = exec_dirname + "/" + gOvsSetupFile
if not os.path.exists(ovsFilename):
    print ""
    print "OVS installation script - "+ gOvsSetupFile + " does not exists in - " + exec_dirname + "\n"
    print "Get file from - https://github.com/yyang13/ovs_nsh_patches/blob/master/start-ovs-deb.sh\n"
    exit(0)

cliFilename   = exec_dirname + "/" + gClientSetupFile
if not os.path.exists(cliFilename):
    print ""
    print "OVS installation script - "+ gClientSetupFile + " does not exists in - " + exec_dirname + "\n"
    exit(0)

ssh_session = ssh_apis.ssh_login(gUserInputData['client']['ip'],gUserInputData['client']['user'],gUserInputData['client']['password'])


ssh_session.sendline ("sudo ovs-vsctl show")
ssh_session.expect (ssh_apis.COMMAND_PROMPT)
outdata = ssh_session.before
if 'ovs_version:' in outdata or 'ovs-vsctl:' in outdata:
    print "Ovs installed on end host. Doing clean and config"
    ssh_apis.ssh_sftp(gUserInputData['client']['ip'],gUserInputData['client']['user'],gUserInputData['client']['password'], cliFilename, "/tmp/"+gClientSetupFile)

    ssh_session.sendline ("sudo sh /tmp/"+gClientSetupFile + " " + gUserInputData['server']['overlay_ip'] + " " + gUserInputData['client']['overlay_ip'], gUserInputData['controller']['ip'] )
    i = ssh_session.expect (ssh_apis.COMMAND_PROMPT)
    outdata = ssh_session.before


else:
    print "Ovs not installed on end host. Doing install and config"
    ssh_apis.ssh_sftp(gUserInputData['client']['ip'],gUserInputData['client']['user'],gUserInputData['client']['password'], ovsFilename, "/tmp/"+gOvsSetupFile)
    ssh_apis.ssh_sftp(gUserInputData['client']['ip'],gUserInputData['client']['user'],gUserInputData['client']['password'], cliFilename, "/tmp/"+gClientSetupFile)

    ssh_session.sendline ("sudo sh /tmp/"+gOvsSetupFile)
    i = ssh_session.expect (ssh_apis.COMMAND_PROMPT)
    outdata = ssh_session.before

    ssh_session.sendline ("sudo sh /tmp/"+gClientSetupFile + " " + gUserInputData['server']['overlay_ip'] + " " + gUserInputData['client']['overlay_ip'], gUserInputData['controller']['ip'] )
    i = ssh_session.expect (ssh_apis.COMMAND_PROMPT)
    outdata = ssh_session.before


ssh_apis.ssh_logout(ssh_session)

