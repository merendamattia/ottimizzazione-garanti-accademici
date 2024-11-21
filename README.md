# pd-project

## Requisiti

È necessario avere i seguenti strumenti installati:

-   [Docker](https://docs.docker.com/engine/install/).
-   [Docker Compose](https://docs.docker.com/compose/install/).
-   [Doxygen](https://doxygen.nl).
-   [Make](https://www.gnu.org/software/make/).

Per verificare la corretta installazione:

```bash
docker --version
docker compose version
doxygen --version
make --version
```

## Build e Run

> Per eseguire questi comandi è necessario trovarsi nella root del progetto.

Per costruire il container:

```bash
docker compose build
```

Per eseguire il container:

```bash
docker compose run pd-project
```

> Potrebbe essere necessario aggiornare i permessi della cartella `src` con `chmod -R 777 src`.

## Documentazione

> Per eseguire questi comandi è necessario trovarsi all'interno della root del progetto.

Per la generazione della documentazione:

```bash
doxygen Doxyfile
cd doc/latex
make
```

La documentazione sarà disponibile in formato:

-   pdf al path [doc/latex/refman.pdf](doc/latex/refman.pdf).
-   web al path [doc/html/index.html](doc/html/index.html).
