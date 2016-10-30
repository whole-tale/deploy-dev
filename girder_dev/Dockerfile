FROM node:5
MAINTAINER Patrick Reynolds <patrick.reynolds@kitware.com>

EXPOSE 8080

RUN apt-get update && apt-get install -qy software-properties-common python-software-properties && \
  apt-get update && apt-get install -qy \
    build-essential \
    git \
    vim \
    libffi-dev \
    libpython-dev && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py

RUN git clone https://github.com/data-exp-lab/girder -b heartbeat
RUN git clone https://github.com/whole-tale/girder_ythub /girder/plugins/ythub

WORKDIR /girder

RUN pip install -e .[plugins]
RUN npm install --unsafe-perm && npm cache clear
RUN npm run build -- --plugins='ythub,oauth,mongo_search,homepage'

COPY ./girder.local.cfg /girder/girder/conf/girder.local.cfg

ENTRYPOINT ["python", "-m", "girder"]
