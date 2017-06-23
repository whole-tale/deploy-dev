FROM girder/girder:latest
MAINTAINER Kacper Kowalik <xarthisius.kk@gmail.com>

RUN git clone https://github.com/whole-tale/girder_ythub /girder/plugins/wholetale
RUN git clone https://github.com/whole-tale/girder_wt_data_manager /girder/plugins/wt_data_manager

WORKDIR /girder

RUN pip install -e .[plugins] -r plugins/wholetale/requirements.txt
RUN girder-install web --all-plugins

COPY ./girder.local.cfg /girder/girder/conf/girder.local.cfg
