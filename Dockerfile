ARG  base_image_tag
FROM ${base_image_tag}

USER root:root
RUN curl --silent --location https://rpm.nodesource.com/setup_18.x | bash -
RUN yum install -y nodejs
USER wmlfuser:condausers
RUN umask 002 && \
pip install javascript

USER wmlfuser:condausers
RUN umask 002 && \
mkdir -p /home/wmlfuser/mypkgs && \
pip install pydot --target /home/wmlfuser/mypkgs
ENV PYTHONPATH=$PYTHONPATH:/home/wmlfuser/mypkgs