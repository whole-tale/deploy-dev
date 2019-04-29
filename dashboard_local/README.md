```
$ docker build -t dashboard_local .
$ docker run --rm -ti -v $PWD:/srv/dashboard -p 4200:80 dashboard_local
$ docker run --rm -ti -v $PWD:/usr/src/node-app risingstack/alpine:3.7-v8.10.0-4.8.0 ./node_modules/.bin/ember build --environment=development
