#!/bin/sh

domain=local.wholetale.org
role=manager,celery
image=wholetale/gwvolman:latest
registry_user=fido
registry_pass=secretpass

sudo umount /usr/local/lib > /dev/null 2>&1 || true
docker stop -t 0 celery_worker >/dev/null 2>&1
docker rm celery_worker > /dev/null 2>&1

# docker pull ${image} > /dev/null 2>&1
# Do not set GIRDER_API_URL for celery_worker it's handled elsewhere for local deployment
# See my comment: https://github.com/whole-tale/deploy-dev/issues/10#issuecomment-451193663

docker run \
    --name celery_worker \
    --label traefik.enable=false \
    -e HOSTDIR=/host \
    -e DOMAIN=${domain} \
    -e TRAEFIK_NETWORK=wt_traefik-net \
    -e TRAEFIK_ENTRYPOINT=https \
    -e REGISTRY_USER=${registry_user} \
    -e REGISTRY_URL=https://registry.${domain} \
    -e REGISTRY_PASS=${registry_pass} \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    -v /:/host \
    -v /var/cache/davfs2:/var/cache/davfs2 \
    -v /run/mount.davfs:/run/mount.davfs \
    -v $PWD/src/gwvolman:/gwvolman \
    --device /dev/fuse \
    --cap-add SYS_ADMIN \
    --cap-add SYS_PTRACE \
    --network wt_celery \
    -d ${image} \
      -Q ${role},$(docker info --format "{{.Swarm.NodeID}}") \
      --hostname=$(docker info --format "{{.Swarm.NodeID}}")

docker exec -ti celery_worker chown davfs2:davfs2 /host/run/mount.davfs
docker exec -ti celery_worker chown davfs2:davfs2 /host/var/cache/davfs2
