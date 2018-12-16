FROM wholetale/girder:latest

COPY --chown=root:root ./docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["girder", "serve"]