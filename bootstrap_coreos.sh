docker run -ti --rm -v /opt/bin:/out ubuntu:14.04 /bin/bash -c "apt-get update -qqy && 
  apt-get -y install make wget &&
  cp /usr/bin/make /out/bin && 
  cp /lib/x86_64-linux-gnu/libtinfo.so.5 /out && 
  chmod +x /out/libtinfo.so.5 && 
  wget https://bitbucket.org/pypy/pypy/downloads/pypy2-v6.0.0-linux64.tar.bz2 && 
  tar --strip-components=1 -xvf pypy2-v6.0.0-linux64.tar.bz2 -C /out && 
  ln -s /out/python pypy"
/opt/bin/python -m ensurepip --user
/opt/bin/python -m pip install requests --user
