# pd-project
Realizzato da:
- Colli Simone
- Merenda Saverio Mattia

## Requisiti
È necessario avere i seguenti strumenti installati:

-   [Docker](https://docs.docker.com/engine/install/)
-   [Docker Compose](https://docs.docker.com/compose/install/)

Per verificare la corretta installazione:

```bash
docker --version
docker compose version
```

## Build e Run
Per costruire il container:

```bash
docker compose build --no-cache
```

Per eseguire il container:

```bash
docker compose run pd-project
```

> Potrebbe essere necessario aggiornare i permessi della cartella `src` con `chmod -R 777 src`.

## Documentazione
Per generare la documentazione è necessario avere installato:
- [Doxygen](https://doxygen.nl)
- [Make](https://www.gnu.org/software/make/)

Successivamente eseguire:
```bash
doxygen Doxyfile
cd doc/latex
make
```
