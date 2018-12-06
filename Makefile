.PHONY: clean dirs dev images
SUBDIRS = ps homes src

images:
	docker pull traefik:alpine
	docker pull mongo:3.2
	docker pull redis:latest
	docker pull registry:2.6
	docker pull wholetale/girder:latest
	docker pull wholetale/dashboard:latest
	docker pull wholetale/gwvolman:latest

sources:
	git clone https://github.com/whole-tale/gwvolman src/gwvolman
	git clone https://github.com/whole-tale/girder_wholetale src/wholetale
	git clone https://github.com/whole-tale/girder_wt_data_manager src/wt_data_manager
	git clone https://github.com/whole-tale/wt_home_dirs src/wt_home_dir

dirs: $(SUBDIRS)

$(SUBDIRS):
	@mkdir $@

services: dirs sources images

dev:
	docker stack deploy --compose-file=docker-stack.yml wt
	./run_worker.sh
	cid=$$(docker ps --filter=name=wt_girder -q);
	while [ -z $${cid} ] ; do \
		  echo $${cid} ; \
		  sleep 1 ; \
	    cid=$$(docker ps --filter=name=wt_girder -q) ; \
	done; \
	true
	docker exec --user=root -ti $$(docker ps --filter=name=wt_girder -q) pip install -e /gwvolman
	docker exec -ti $$(docker ps --filter=name=wt_girder -q) girder-install web --dev --plugins=oauth,gravatar,jobs,worker,wt_data_manager,wholetale,wt_home_dir
	./setup_girder.py

clean:
	-./stop_worker.sh
	-./destroy_instances.py
	-docker stack rm wt
	-docker volume rm wt_mongo-cfg wt_mongo-data
