Setting up local testing instance of Girder
===========================================

Requirements:

 * docker >= 1.12
 * docker-compose >= 1.8.0
 * requests (`pip install requests --user`)

Clone this repository:

```
git clone https://github.com/whole-tale/girder_deploy
```

Go to `ythub_test` directory and run:

```
cd girder_deploy/ythub_test
docker pull xarthisius/ythub-jupyter
docker-compose pull
docker-compose build
docker-compose up -d mongodb

# This ^^ may take a while. It's best to monitor progress via:
#  docker-compose logs -f mongodb
# When following message appears:
# ... [initandlisten] waiting for connections on port 27017
# You can proceed starting the rest of the services

docker-compose up -d
```

Add the output of the following command to your `/etc/hosts`

```
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}} {{.Name}}' proxy girder || tr '/' ' '
```

Lastly, run `python setup_girder.py`.

If you follow `http://localhost:8080/` you should be greeted by Girder's
homepage.
