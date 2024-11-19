FROM ubuntu:23.10


RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y gringo python3 python3-pip \
    nano time curl htop

# User
RUN useradd -ms /bin/bash clingo

# Directory used for setup phase
ARG SETUPDIR="/home/clingo/setup"
RUN mkdir -p ${SETUPDIR}
WORKDIR ${SETUPDIR}

COPY pip-requirements.txt pip-requirements.txt
RUN pip install --break-system-packages -r pip-requirements.txt

# Workdir
ARG WORKDIR="/home/clingo/code"
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

# Permissions
RUN chown -R clingo:clingo ${WORKDIR}
RUN chmod -R 755 ${WORKDIR}


# User
USER clingo
