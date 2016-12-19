#!/usr/bin/python
import requests,json
import sys, os, re
from pprint import pprint
#import paramiko
import traceback, logging
import ssh_apis
import pexpect


#Global data
gUserInputData          = ""
gOdlSetupFile           = "clean_install_odl.sh" 
gOdlCleanStartFile      = "clean_start_odl.sh" 
gOdlDefaultDist         = "https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/distribution-karaf/0.5.1-Boron-SR1/distribution-karaf-0.5.1-Boron-SR1.tar.gz"
gOdlDefaultBaseDir      = "sfc-demo-root"
gOdlExpectTimeout       = 330

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
    print "Starting ODL setup..."
    #print gUserInputData['odl-configuration']['service-function-forwarders'][1]['ip-address']

#create outpur file name as script_folder + output.py
exec_dirname  = os.path.dirname(os.path.realpath(sys.argv[0]))

odlSetupFile   = exec_dirname + "/" + gOdlSetupFile
if not os.path.exists(odlSetupFile):
    print ""
    print "ODL setup file - "+ gOdlSetupFile + " does not exists in - " + exec_dirname + "\n"
    exit(0)

odlStartFile   = exec_dirname + "/" + gOdlCleanStartFile
if not os.path.exists(odlStartFile):
    print ""
    print "ODL clean start file - "+ gOdlSetupFile + " does not exists in - " + exec_dirname + "\n"
    exit(0)


ssh_session = ssh_apis.ssh_login(gUserInputData['controller']['ip'],gUserInputData['controller']['user'],gUserInputData['controller']['password'])

if gUserInputData['controller']['base_dir'] == "":
    ssh_session.sendline ("if test -f $HOME/"+ gOdlDefaultBaseDir +"/sfc-karaf/target/assembly/version.properties; then echo YESSSSS; else echo NOOOOO; fi ") 
else:
    ssh_session.sendline ("if test -f $HOME/"+  gUserInputData['controller']['base_dir'] +"/sfc-karaf/target/assembly/version.properties; then echo YESSSSS; else echo NOOOOO; fi ") 

ssh_session.expect (ssh_apis.COMMAND_PROMPT)
outdata = ssh_session.before.split('\r')

if 'YESSSSS' in outdata[-2]:
    print "ODL installed on end host. Doing stop and start"
    ssh_apis.ssh_sftp(gUserInputData['controller']['ip'],gUserInputData['controller']['user'],gUserInputData['controller']['password'], odlStartFile, "/tmp/"+gOdlCleanStartFile)
   
    if gUserInputData['controller']['dist'] == "":
        if gUserInputData['controller']['base_dir'] == "":
            ssh_session.sendline ("sh /tmp/"+gOdlCleanStartFile + " " + gOdlDefaultDist + " " + gOdlDefaultBaseDir+ " " + gUserInputData['controller']['ip']) 
        else:
            ssh_session.sendline ("sh /tmp/"+gOdlCleanStartFile + " " + gOdlDefaultDist + " " + gUserInputData['controller']['base_dir']+ " " + gUserInputData['controller']['ip']) 
    else:
        if gUserInputData['controller']['base_dir'] == "":
            ssh_session.sendline ("sh /tmp/"+gOdlCleanStartFile + " " + gUserInputData['controller']['dist'] + " " + gOdlDefaultBaseDir+ " " + gUserInputData['controller']['ip']) 
        else:
            ssh_session.sendline ("sh /tmp/"+gOdlCleanStartFile + " " + gUserInputData['controller']['dist'] + " " + gUserInputData['controller']['base_dir']+ " " + gUserInputData['controller']['ip']) 
    i = ssh_session.expect (ssh_apis.COMMAND_PROMPT, timeout=gOdlExpectTimeout)
    #i = ssh_session.expect(pexpect.EOF, timeout=None)
    outdata = ssh_session.before
        

else:
    print "ODL not installed on end host. Doing install and config"
    ssh_apis.ssh_sftp(gUserInputData['controller']['ip'],gUserInputData['controller']['user'],gUserInputData['controller']['password'], odlStartFile, "/tmp/"+gOdlCleanStartFile)
    ssh_apis.ssh_sftp(gUserInputData['controller']['ip'],gUserInputData['controller']['user'],gUserInputData['controller']['password'], odlSetupFile, "/tmp/"+gOdlSetupFile)

    #install odl
    if gUserInputData['controller']['dist'] == "":
        if gUserInputData['controller']['base_dir'] == "":
            ssh_session.sendline ("sh /tmp/"+gOdlSetupFile + " " + gOdlDefaultDist + " " + gOdlDefaultBaseDir+ " " + gUserInputData['controller']['ip']) 
        else:
            ssh_session.sendline ("sh /tmp/"+gOdlSetupFile + " " + gOdlDefaultDist + " " + gUserInputData['controller']['base_dir']+ " " + gUserInputData['controller']['ip']) 
    else:
        if gUserInputData['controller']['base_dir'] == "":
            ssh_session.sendline ("sh /tmp/"+gOdlSetupFile + " " + gUserInputData['controller']['dist'] + " " + gOdlDefaultBaseDir+ " " + gUserInputData['controller']['ip']) 
        else:
            ssh_session.sendline ("sh /tmp/"+gOdlSetupFile + " " + gUserInputData['controller']['dist'] + " " + gUserInputData['controller']['base_dir']+ " " + gUserInputData['controller']['ip']) 
    i = ssh_session.expect (ssh_apis.COMMAND_PROMPT,timeout=gOdlExpectTimeout)
    #i = ssh_session.expect(pexpect.EOF, timeout=None)
    outdata = ssh_session.before

    #stop start odl
    if gUserInputData['controller']['dist'] == "":
        if gUserInputData['controller']['base_dir'] == "":
            ssh_session.sendline ("sh /tmp/"+gOdlCleanStartFile + " " + gOdlDefaultDist + " " + gOdlDefaultBaseDir+ " " + gUserInputData['controller']['ip']) 
        else:
            ssh_session.sendline ("sh /tmp/"+gOdlCleanStartFile + " " + gOdlDefaultDist + " " + gUserInputData['controller']['base_dir']+ " " + gUserInputData['controller']['ip']) 
    else:
        if gUserInputData['controller']['base_dir'] == "":
            ssh_session.sendline ("sh /tmp/"+gOdlCleanStartFile + " " + gUserInputData['controller']['dist'] + " " + gOdlDefaultBaseDir+ " " + gUserInputData['controller']['ip']) 
        else:
            ssh_session.sendline ("sh /tmp/"+gOdlCleanStartFile + " " + gUserInputData['controller']['dist'] + " " + gUserInputData['controller']['base_dir']+ " " + gUserInputData['controller']['ip']) 

    i = ssh_session.expect (ssh_apis.COMMAND_PROMPT, timeout=gOdlExpectTimeout)
    #i = ssh_session.expect(pexpect.EOF, timeout=None)
    outdata = ssh_session.before


ssh_apis.ssh_logout(ssh_session)
