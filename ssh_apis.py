
import pexpect 
import paramiko
import sys, os 

COMMAND_PROMPT = '[#$] '
TERMINAL_PROMPT = '(?i)terminal type\?'
TERMINAL_TYPE = 'vt100'

SSH_NEWKEY = '(?i)are you sure you want to continue connecting'

## Login via SSH
def ssh_login (host, user, password):
    global SSH_NEWKEY, COMMAND_PROMPT
    print "Login " + host
    child = pexpect.spawn('ssh -l %s %s'%(user, host))
    i = child.expect([pexpect.TIMEOUT, SSH_NEWKEY, COMMAND_PROMPT, '(?i)password'])
    if i == 0:
        print 'ERROR! could not login with SSH. Here is what SSH said:'
        print child.before, child.after
        print str(child)
        sys.exit (1)
    if i == 1: # In this case SSH does not have the public key cached.
        child.sendline ('yes')
        child.expect ('(?i)password')
    if i == 2:
        # This may happen if a public key was setup to automatically login.
        # But beware, the COMMAND_PROMPT at this point is very trivial and
        # could be fooled by some output in the MOTD or login message.
        pass
    if i == 3:
        child.sendline(password)
        # Now we are either at the command prompt or
        # the login process is asking for our terminal type.
        i = child.expect ([COMMAND_PROMPT, TERMINAL_PROMPT])
        if i == 1:
            print "Sending terminal type...."
            child.sendline (TERMINAL_TYPE)
            child.expect (COMMAND_PROMPT)
    return child
'''
        COMMAND_PROMPT = "PEXPECT$"
        print "PS1="+COMMAND_PROMPT 
        child.sendline ("PS1="+COMMAND_PROMPT) # In case of sh-style
        i = child.expect ([pexpect.TIMEOUT, COMMAND_PROMPT], timeout=10)
        if i == 0:
            print "# Couldn't set sh-style prompt -- trying csh-style."
            child.sendline ('set prompt=\'[PEXPECT]\$\'')
            i = child.expect ([pexpect.TIMEOUT, COMMAND_PROMPT], timeout=10)
            if i == 0:
                print "Failed to set command prompt using sh or csh style."
                print "Response was:"
                print child.before
                sys.exit (1)
'''

def ssh_logout(child):
# Now exit the remote host.
        child.sendline ('exit')
        index = child.expect([pexpect.EOF, "(?i)there are stopped jobs"])
        if index==1:
            child.sendline("exit")
            child.expect(EOF)

def ssh_sftp(host, user, passwd, src_file, dst_file):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=passwd)
    sftp = ssh.open_sftp()
    sftp.put(src_file, dst_file)
    sftp.close()
    ssh.close()
