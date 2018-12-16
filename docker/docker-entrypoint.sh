#!/bin/bash

if [ "$HOST_UID" == "" ]; then
    echo "Missing HOST_UID!"
    sleep 120
else
    usermod -u $HOST_UID girder
    groupmod -g $HOST_GID girder
fi

# add a password and enable login because the gridftp server 
# refuses to start if the user account is disabled; it also
# refuses to start with a message about the login being disabled
# even if passwd -S shows a proper 'P' if the user has the default
# system shell, which corresponds to a blank shell in /etc/passwd, 
# because gridfpt has its own standards
# (see globus_i_gfs_data.c: globus_l_gfs_validate_pwent() and man 5 passwd)
STATUS=`passwd -S girder | awk '{print $2}'`
if [ "$STATUS" == "L" ]; then
    usermod -p `openssl rand -base64 32` girder
    usermod -U girder
fi
usermod -s /bin/bash girder

exec sudo -u girder "$@"

