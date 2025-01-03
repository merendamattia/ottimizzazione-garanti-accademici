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
COPY .github/REQUIREMENTS-PIP requirements-pip.txt
RUN pip install --break-system-packages -r requirements-pip.txt

# Configurazione della directory di lavoro principale
ARG WORKDIR="/home/clingo/src"
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

# Configurazione dei permessi
RUN chown -R clingo:clingo ${WORKDIR}
RUN chmod -R 755 ${WORKDIR}

# Configurazione dei colori per la bash
RUN echo 'PS1="\[\033[01;34m\]\u@\h:\[\033[01;32m\]\w\[\033[00m\]\$ "' >> /home/clingo/.bashrc && \
    echo 'alias ll="ls -lh --color=auto"' >> /home/clingo/.bashrc && \
    echo 'alias la="ls -lha --color=auto"' >> /home/clingo/.bashrc && \
    echo 'export LS_COLORS="di=01;34:ln=01;36:so=01;35:pi=33:ex=01;32:bd=40;33;01:cd=40;33;01"' >> /home/clingo/.bashrc

# Passaggio all'utente non root
USER clingo
