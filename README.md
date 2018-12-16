Setting up a local instance of Whole Tale
=========================================

This directory contains scripts required to run a full instance of the
Whole Tale platform on a single system (e.g., laptop or VM). The
installation uses a predefined domain `*.local.wholetale.org` which maps
to localhost. This means that VM-based installations will require port
forwarding to access (see below).


System requirements
-------------------
 * Linux (tested on Ubuntu 18.04, CoreOS; not working on MacOS _yet_)
 * docker 17.04.0+, swarm mode
 * python, requests
 * make (optional)
 * acme.tar (SSL keys for local.wholetale.org; ask on slack)
 * Globus auth registration. You must have a registered app on [Globus](https://developers.globus.org) with the callback set to `https://girder.local.wholetale.org/api/v1/oauth/globus/callback`
 * Default user with uid:1000 and gid:1000 (this does not seem to be necessary; works with uid=gid=1001)
 * Nothing running on 80 or 443 (i.e., stop your local instance of apache)
  
 
Deployment process
------------------
The deployment process does the following:
* Pulls all required images
* Starts the WT stack via Docker swarm
* Starts the Celery worker (`gwvolman`)
    * **WARNING:** This container has fairly elavated privileges:
        *  it has access to host's filesystem
        *  it can perform multiple system calls as de facto host's root
    * **WARNING:** During `celery_worker`'s initialization host's `/usr/local` directory is overshadowed by the content of `/usr/local` from the container. 
* Runs `setup_girder.py` to initialize the instance

If you haven't already, initialize your system as a swarm master:
```
docker swarm init
```

Add default user (1000) and group (100), if not present:
```
[[ -z $(getent group 100) ]] && sudo groupadd -g 100 wtgroup
[[ -z $(getent passwd 1000) ]] && sudo useradd -g 100 -u 1000 wtuser
```

Export your Github Oauth ID and secret:
```
export GLOBUS_CLIENT_ID=<client ID>
export GLOBUS_CLIENT_SECRET=<client secret>
```

Create a `certs` directory and copy `acme.tar` to it.

Clone this repository and  run `make dev`:
```
git clone https://github.com/whole-tale/deploy-dev
cd deploy-dev/
make dev
```

To confirm things are working, all `REPLICAS` should show `1/1`
```
$ docker service ls
ID                  NAME                MODE                REPLICAS            IMAGE                        PORTS
jpzhf12jh6wj        wt_dashboard        replicated          1/1                 wholetale/dashboard:latest
26gv8qfb85sq        wt_girder           replicated          1/1                 wholetale/girder:latest
irdizcla8jal        wt_mongo            replicated          1/1                 mongo:3.2
p46dbxbgcae3        wt_redis            replicated          1/1                 redis:latest
vyf55zx0x95y        wt_registry         replicated          1/1                 registry:2.6                 *:443->443/tcp
41u4zyqrrv79        wt_traefik          replicated          1/1                 traefik:alpine               *:80->80/tcp, *:8080->8080/tcp
```

The `celery_worker` runs outside of swarm, confirm that it's running:
```
$ docker ps | grep celery_worker
0e8124024f03        wholetale/gwvolman:latest                                "python3 -m girder_w…"   15 hours ago        Up 15 hours                             celery_worker
```

Note: If you're running in a VM, you'll need to setup  forwarding for port 80 (requires `sudo`):
```
$ sudo ssh -L 80:localhost:80 user@VM
```


You should now be able to open a browser to https://dashboard.local.wholetale.org to access your running instance of Whole Tale.  



Uninstall
---------

The following will remove all services and delete the volume data:

```
make clean
```

Some notes on Globus
--------------------

There are a number of changes that are needed to get globus to work. One
is that the GridFTP server (used by Globus Connect Personal) refuses to
start as root. The second is that it refuses connections if the user
account that the GridFTP login maps to is disabled. Well, that's what the
error message says, but what it does check is whether the user has a
non-empty shell in /etc/passwd. Linux interprets an empty shell in
/etc/passwd as the default system shell rather than a disabled account,
so this should probably be fixed in GridFTP. In any event, this branch
does the following in this regard:
 * Run girder (and hence Globus Connect) as the user 'girder'
 * Add a random password to the 'girder' account and enable the account
 (usermod -U)
 * Set the shell for 'girder' to '/bin/bash'
 * Change the UID:GID for girder:girder inside the container to match the
 UID:GID of the host account so that the container can properly access
 mounted directories. It's hard to believe Docker doesn't have a
 mechanism to deal with this properly.

These steps are taken in '/usr/local/bin/docker-entrypoint.sh', a copy of
which can be found in the 'docker' directory. Since this is the entry
point for the image, this file must be put in there when the image is
made. The particular version of the deployment environment uses an image
under my personal namespace. This needs to be changed if you want to make
any  changes to the image.

Of course, using Globus transfer means that Globus Auth must be used for
authentication, which, in turn, means that proper certs must be used for
the deployment (unless you can convince your browser otherwise). So see
instructions above about 'acme.tar'.

To test the Globus transfers, start the contraption using 'make dev', log
in to 'https://dashboard.local.wholetale.org' using your favorite
browser, obtain the Girder token, put it in the 'GIRDER_TOKEN'
environment variable, then run 'test_globus.py'. After some time you
should see the transfer in 'Activity' at 'app.globus.org' and after some
more time you should see the file appearing inside the 'ps' directory
under a cryptic name and inside some nested directories.