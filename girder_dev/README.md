Setting up local testing instance of Girder
===========================================

Requirements:

 * docker >= 1.12
 * docker-compose >= 1.8.0

Clone this repository:

```
git clone https://github.com/whole-tale/girder_deploy
```

Go to `girder_dev` directory and run:

```
cd girder_deploy/girder_dev
docker-compose build
docker-compose up -d
```

Add the output of the following command to your `/etc/hosts` (make sure to
remove trailing slashes from hostnames):

```
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}} {{.Name}}' proxy girder
```

If you follow `http://localhost:8080/` you should be greeted by Girder's
homepage. 

 1. Create a user acount, first one has always admin priviledges.
 
 2. Go to `http://localhost:8080/#plugins` and enable ythub plugin. After
    mandatory server restart (big red button on top of the plugin page), go to
    configuration page of the ythub plugin
    `http://localhost:8080/#plugins/ythub/config`. Set `tmpnb URL` to
    `http://proxy:8000/`. Hit 'Generate Key' button, set heartbeat to 15.

 3. Go to `http://localhost:8080/#assetstores` and create default filesysystem
    assetstore with path: `/mnt/girder`

You should be good to go at this point, enjoy!
