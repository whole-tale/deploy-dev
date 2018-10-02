.PHONY: clean dirs dev images
SUBDIRS = ps homes

images:
	docker pull traefik:alpine
	docker pull mongo:3.2
	docker pull redis:latest
	docker pull registry:2.6
	docker pull wholetale/girder:latest
	docker pull wholetale/dashboard:latest
	docker pull wholetale/gwvolman:latest

dirs: $(SUBDIRS)

$(SUBDIRS):
	@mkdir $@

dev: dirs images
	docker stack deploy --compose-file=docker-stack.yml wt
	./run_worker.sh
	./setup_girder.py

clean:
	-./stop_worker.sh
	-docker stack rm wt
	-docker volume rm wt_mongo-cfg wt_mongo-data

