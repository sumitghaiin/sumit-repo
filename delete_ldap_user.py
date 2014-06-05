#!/usr/bin/python
import os, sys, getpass, subprocess
#who is to be removed from lday?
uname = raw_input('Which user is to be removed? ')
#get a password, don't show keystrokes
root_pass = getpass.getpass("enter ldap password for root ")
deletecmd = '/usr/bin/ldapdelete -x -w %s -D "cn=root,dc=aers,dc=local" "uid=%s,ou=People,dc=aers,dc=local"' % (root_pass,uname)
deletecode = subprocess.call(deletecmd, shell=True)
if deletecode > 0:
    print "error code %s" % deletecode
    sys.exit (1);
print 'User %s has been removed from the system, their homespace probably still exists and should be archived.' % uname 
