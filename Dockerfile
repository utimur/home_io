FROM klyushinmisha/home_io_bootstrap

WORKDIR /opt/home_io_backend

# install deps
ARG REQUIREMENTS
COPY ${REQUIREMENTS} .
RUN pip3 install -r ${REQUIREMENTS}

# copy files
ARG CONFIG
COPY run_app.sh .
COPY env.py .
COPY config/${CONFIG} ./config.py
RUN touch __init__.py