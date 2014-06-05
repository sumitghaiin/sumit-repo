#!/usr/bin/python
#!/usr/bin/python
import os, getpass, subprocess, sys

# ensure we are root
if not os.geteuid()==0:
    sys.exit("\nOnly root can run this script\n")

# make sure there is no existing ldiff file
os.remove ('/tmp/newuser.ldiff')

#what username are we adding today?
uname = raw_input('What will be the users username? ')

#get the largest uid and add one to it
command = "getent passwd | grep -v nobody | awk -F: '{print $3}' | sort -n | tail -1"
maxuid = os.popen(command).read()
maxuid = int(maxuid)
newuid = maxuid + 1
ldiff='\ndn: uid=%s,ou=People,dc=aers,dc=local\nuid: %s\ncn: %s\nobjectClass: account\nobjectClass: posixAccount\nobjectClass: top\nobjectClass: shadowAccount\nuserPassword: e2NyeXB0fSQxJDhiaFhxNkFEJEFCbk1OcXpLNFVZaERUYlJhZExaNDA=\nshadowLastChange: 13080\nshadowMax: 99999\nshadowWarning: 7\nloginShell: /bin/bash\nuidNumber: %d\ngidNumber: 100\nhomeDirectory: /home/%s' % (uname,uname,uname,newuid,uname)
newuser_ldiff = open('/tmp/newuser.ldiff', 'a')
newuser_ldiff.write(ldiff)
newuser_ldiff.close()

#get a password, don't show keystrokes
ldap_pass = getpass.getpass("enter ldap password for root")

#attempt to add the user
print "\n#################### adding user ############################\n"
ldapadd = 'ldapadd -x -w %s -D "cn=root,dc=aers,dc=local" -f /tmp/newuser.ldiff' % (ldap_pass)
addcode = subprocess.call(ldapadd, shell=True)

if addcode > 0:
    print >>sys.stderr, "Child was terminated by signal", -addcode
    sys.exit(1);

#if the previous step was successful, then set a password
print "\n#################### setting password #######################\n"
ldappasswd = '/usr/bin/ldappasswd -x -w %s -D "cn=root,dc=aers,dc=local" -s aers1234 "uid=%s,ou=People,dc=aers,dc=local"' % (ldap_pass,uname)
passwdcode = subprocess.call(ldappasswd, shell=True)
if passwdcode > 0:
    print >>sys.stderr, "Child was terminated by signal", -passwdcode
    sys.exit(2);

#if the previous step was successful, then make the home space
print "\n#################### make homespace #########################\n"
mkdircode = subprocess.call("mkdir" + " /home/" + uname, shell=True)
if mkdircode > 0:
    print >>sys.stderr, "Child was terminated by signal", -mkdircode
    sys.exit(3);

#if the previous step was successful, then et the permissions on home space
print "\n#################### chown homespace ########################\n"
chowncode = subprocess.call("chown " + uname + " /home/" + uname, shell=True)
if chowncode > 0:
    print >>sys.stderr, "Child was terminated by signal", -chowncode
    sys.exit(4);
