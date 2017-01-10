#!/usr/bin/python
import requests,json
import sys, os, re
from pprint import pprint
#import paramiko
import traceback, logging
import ssh_apis

#Global data
gUserInputData      = ""
gSfcSetupFile    = "sfcagent-boronpatch-0.1.4.tar.gz" 


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

sfcFilename   = exec_dirname + "/" + gSfcSetupFile
if not os.path.exists(sfcFilename):
    print ""
    print "SFC agent package - "+ gSfcSetupFile + " does not exists in - " + exec_dirname + "\n"
    exit(0)

for node in gUserInputData['SF']:
    #print "Login to " + node['ip'] 
    ssh_session = ssh_apis.ssh_login(node['ip'],node['user'],node['password'])

    print "starting installation of required packages.."
    ssh_session.sendline ("sudo apt-get install -y python-pip")
    i = ssh_session.expect (ssh_apis.COMMAND_PROMPT)
    outdata = ssh_session.before
    ssh_session.sendline ("sudo apt-get install -y git")
    i = ssh_session.expect (ssh_apis.COMMAND_PROMPT)
    outdata = ssh_session.before


    ssh_session.sendline ("sudo pkill -f sfc_agent.py")
    i = ssh_session.expect (ssh_apis.COMMAND_PROMPT)
    outdata = ssh_session.before

    #print "starting uninstall.."
    ssh_session.sendline ("sudo pip3 uninstall sfc -y")
    i = ssh_session.expect (ssh_apis.COMMAND_PROMPT)
    outdata = ssh_session.before

    #print "copying file.."    
    ssh_apis.ssh_sftp(node['ip'],node['user'],node['password'], sfcFilename, "/tmp/"+gSfcSetupFile)

    #print "starting install"
    #print "cd /tmp/; sudo pip3 install " + gSfcSetupFile
    ssh_session.sendline ("cd /tmp/; sudo pip3 install " + gSfcSetupFile )
    i = ssh_session.expect (ssh_apis.COMMAND_PROMPT)
    outdata = ssh_session.before

    ssh_session.sendline ("cd /usr/local/lib/python3.4/dist-packages/sfc")
    i = ssh_session.expect (ssh_apis.COMMAND_PROMPT)
    outdata = ssh_session.before

    ssh_session.sendline ("sudo python3.4 ./sfc_agent.py --rest --odl-ip-port " + gUserInputData['controller']['ip'] + ":8181 &")
    i = ssh_session.expect (ssh_apis.COMMAND_PROMPT)
    outdata = ssh_session.before

    ssh_apis.ssh_logout(ssh_session)

