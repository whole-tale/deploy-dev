#!/bin/bash

docker stop -t 0 celery_worker >/dev/null 2>&1 || true
docker rm celery_worker > /dev/null 2>&1 || true
