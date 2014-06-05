#!/bin/bash
umask 007
cd /var/lib/svn/reps
svnadmin create $1
ln -s /var/lib/svn/scripts/hooks/post-commit /var/lib/svn/reps/$1/hooks/
chown -R svn:ldapuser /var/lib/svn/reps/$1

ssh n.tor /homes/jbresciani/scripts/create_tor_repo.sh $1

cd /tmp
mkdir svntmp
cd svntmp
mkdir branches tags trunk vendor
svn import -m 'Initial directory structure' . svn+ssh://svn/$1
cd /
rm -rf /tmp/svntmp
