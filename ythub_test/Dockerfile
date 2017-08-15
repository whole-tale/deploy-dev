FROM xarthisius/girder

RUN git clone https://github.com/data-exp-lab/girder_ythub plugins/ythub
RUN girder-install plugin plugins/ythub
RUN girder-install web --all-plugins

COPY ./girder.local.cfg /girder/girder/conf/girder.local.cfg

ENTRYPOINT ["python3", "-m", "girder"]
