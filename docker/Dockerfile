FROM wholetale/girder:latest

RUN apt-get update && apt-get install sudo vim

COPY --chown=root:root ./docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
COPY ./globus_provider.py /girder/plugins/wholetale/server/lib/globus/globus_provider.py

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["girder", "serve"]