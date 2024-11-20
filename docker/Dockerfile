FROM ubuntu:latest

# Installazione dei pacchetti di sistema
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
        gringo \
        python3 \
        python3-pip \
        nano \
        time \
        curl \
        htop && \
    apt-get clean

# Creazione di un utente non root
RUN useradd -ms /bin/bash clingo

# Configurazione della directory di setup
ARG SETUPDIR="/home/clingo/setup"
RUN mkdir -p ${SETUPDIR}
WORKDIR ${SETUPDIR}

# Copia e installazione delle dipendenze Python
COPY pip-requirements.txt pip-requirements.txt
RUN pip install --break-system-packages -r pip-requirements.txt

# Configurazione della directory di lavoro principale
ARG WORKDIR="/home/clingo/code"
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

# Configurazione dei permessi
RUN chown -R clingo:clingo ${WORKDIR}
RUN chmod -R 755 ${WORKDIR}

# Passaggio all'utente non root
USER clingo
