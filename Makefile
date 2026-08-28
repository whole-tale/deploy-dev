.PHONY: clean dirs dev images gwvolman_src wholetale_src dms_src home_src sources_wt \
	rebuild_dashboard watch_dashboard \
	restart_worker restart_girder globus_handler_src status update_src certs

# Source .env, then the gitignored .env.local, so machine-specific overrides win
# over the shared defaults. Use it for the src_* variables in docker-stack.yml to
# point a plugin mount at a local checkout instead of the clone under ./src.
ENV = { [ -f ./.env ] && . ./.env; [ -f ./.env.local ] && . ./.env.local; true; }

SUBDIRS = src volumes/ps volumes/workspaces volumes/homes volumes/base volumes/versions volumes/runs volumes/licenses volumes/mountpoints volumes/tmp volumes/minio
TAG = latest
MEM_LIMIT = 2048
NODE = node --max_old_space_size=${MEM_LIMIT}
NG = ${NODE} ./node_modules/@angular/cli/bin/ng
YARN = /usr/local/bin/yarn

images:
	docker pull traefik:v3.6
	docker pull node:22-bookworm
	docker pull mongo:4.4
	docker pull redis:7-bullseye
	docker pull registry:2.8
	docker pull python:3.12-slim
	docker pull xarthisius/wt-instance-logger:latest
	docker pull xarthisius/wt-custom-errors:latest
	docker pull xarthisius/girder:5-dev
	docker pull xarthisius/gwvolman:latest
	docker pull xarthisius/repo2docker_wholetale:$(TAG)
	docker pull wholetale/ngx-dashboard:latest

.env:
	curl -s -o .env https://wt.xarthisius.xyz/wt_local_env

traefik/certs:
	mkdir -p traefik/certs

traefik/certs/fullchain.pem: traefik/certs
	curl -s -o traefik/certs/fullchain.pem https://wt.xarthisius.xyz/wt_local_cert

traefik/certs/privkey.pem: traefik/certs
	curl -s -o traefik/certs/privkey.pem https://wt.xarthisius.xyz/wt_local_key

certs: .env traefik/certs/fullchain.pem traefik/certs/privkey.pem

src/aimdl-projects:
	git clone https://github.com/hemi-ncsa-dt/aimdl-projects src/aimdl-projects
	docker run \
		--rm \
		--user=$${UID}:$${GID} \
		-ti \
		-e NODE_OPTIONS=--max-old-space-size=4096 \
		-v $${PWD}/src/aimdl-projects:/srv/app \
		--entrypoint /bin/sh \
		-w /srv/app node:22-bookworm \
			-c 'npm ci --only=production=false'

src/girder-sem-viewer:
	@$(ENV); [ -n "$$src_girder_sem_viewer" ] || git clone https://github.com/htmdec/girder-sem-viewer src/girder-sem-viewer

src/girder-sample-tracker:
	@$(ENV); [ -n "$$src_girder_sample_tracker" ] || git clone https://github.com/htmdec/girder-sample-tracker src/girder-sample-tracker

src/girder-jsonforms:
	@$(ENV); [ -n "$$src_girder_jsonforms" ] || git clone https://github.com/Xarthisius/girder-jsonforms -b igsn src/girder-jsonforms

src/girder-dashboards:
	@$(ENV); [ -n "$$src_girder_dashboards" ] || git clone https://github.com/Xarthisius/girder-dashboards src/girder-dashboards

src/girder-dashboards-precipitate:
	@$(ENV); [ -n "$$src_girder_dashboards_precipitate" ] || git clone https://github.com/imqcam/girder-dashboards-precipitate src/girder-dashboards-precipitate

src/girderfs:
	@$(ENV); [ -n "$$src_girderfs" ] || git clone https://github.com/Xarthisius/girderfs src/girderfs

src/gwvolman:
	@$(ENV); [ -n "$$src_gwvolman" ] || git clone https://github.com/whole-tale/gwvolman src/gwvolman

src/girder-wholetale:
	@$(ENV); [ -n "$$src_girder_wholetale" ] || git clone https://github.com/whole-tale/girder-wholetale src/girder-wholetale

src/girder-virtual-resources:
	@$(ENV); [ -n "$$src_girder_virtual_resources" ] || git clone https://github.com/Xarthisius/girder-virtual-resources src/girder-virtual-resources

src/ngx-dashboard:
	git clone https://github.com/whole-tale/ngx-dashboard src/ngx-dashboard

sources_wt: src src/gwvolman src/girder-wholetale src/girderfs src/ngx-dashboard src/girder-virtual-resources src/girder-sem-viewer src/aimdl-projects src/girder-sample-tracker src/girder-jsonforms src/girder-dashboards src/girder-dashboards-precipitate certs

dirs: $(SUBDIRS)

$(SUBDIRS):
	@mkdir -p $@

services: dirs sources_wt

dev: services
	$(ENV); docker stack config --compose-file docker-stack.yml | docker stack deploy --compose-file - wt
	cid=$$(docker ps --filter=name=wt_girder -q);
	while [ -z $${cid} ] ; do \
		  echo $${cid} ; \
		  sleep 1 ; \
	    cid=$$(docker ps --filter=name=wt_girder -q) ; \
	done; \
	true
	$(ENV); ./setup_girder.py

restart_girder:
	docker exec --user=root -ti $$(docker ps --filter=name=wt_girder -q) touch /venv/lib/python3.12/site-packages/requests/__init__.py

rebuild_dashboard:
	docker run \
		--rm \
		--user=$${UID}:$${GID} \
		-ti \
		-e NODE_OPTIONS=--max-old-space-size=4096 \
		-v $${PWD}/src/ngx-dashboard:/srv/app \
		--entrypoint /bin/sh \
		-w /srv/app node:fermium \
			-c 'yarn install --network-timeout=360000 && \
			./node_modules/@angular/cli/bin/ng build --deleteOutputPath=false --progress'
	sudo touch src/ngx-dashboard/dist/browser/assets/env.js
	sudo chown 101:101 src/ngx-dashboard/dist/browser/assets/env.js

watch_dashboard:
	docker run \
		--rm \
		--user=$${UID}:$${GID} \
		-ti \
		-e NODE_OPTIONS=--max-old-space-size=4096 \
		-v $${PWD}/src/ngx-dashboard:/srv/app \
		-w /srv/app \
		--entrypoint /bin/sh \
		node:fermium \
			-c 'yarn install --network-timeout=360000 && \
			./node_modules/@angular/cli/bin/ng build --watch --poll 15000 --deleteOutputPath=false --progress'

restart_worker:
	docker exec --user=root -ti $$(docker ps --filter=name=wt_girder -q) pip install -e /gwvolman
	docker service update --force --image=$$(docker service inspect wt_celery_worker --format={{.Spec.TaskTemplate.ContainerSpec.Image}}) wt_celery_worker

tail_girder_err:
	docker exec -ti $$(docker ps --filter=name=wt_girder -q) \
		tail -n 200 /home/girder/.girder/logs/error.log

reset_girder:
	docker exec -ti $$(docker ps --filter=name=wt_girder -q) \
		python3 -c 'from girder.models import getDbConnection;getDbConnection().drop_database("girder")'

clean:
	-./destroy_instances.py
	-docker stack rm wt
	limit=15 ; \
	until [ -z "$$(docker service ls --filter label=com.docker.stack.namespace=wt -q)" ] || [ "$${limit}" -lt 0 ]; do \
	  sleep 2 ; \
	  limit="$$((limit-1))" ; \
	done; true
	limit=15 ; \
	until [ -z "$$(docker network ls --filter label=com.docker.stack.namespace=wt -q)" ] || [ "$${limit}" -lt 0 ]; do \
	  sleep 2 ; \
	  limit="$$((limit-1))" ; \
	done; true
	for dir in volumes/mountpoints/* ; do \
	  for subdir in $$dir/* ; do \
	    sudo umount -lf $$subdir || true ; \
	  done \
	done; true
	for dir in ps workspaces homes base versions runs mountpoints ; do \
	  sudo rm -rf volumes/$$dir ; \
	done; true
	-docker volume rm wt_mongo-cfg wt_mongo-data
	rm -rf traefik/certs || true

status:
	@-./scripts/git_status.sh

update_src:
	@-./scripts/git_pull_master.sh
