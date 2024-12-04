# Ottimizzazione dei Garanti accademici

Realizzato da:
- [Colli Simone](https://github.com/SimoneColli)
- [Merenda Saverio Mattia](https://github.com/merendamattia)

Questo lavoro presenta l'analisi e l'implementazione di un sistema automatizzato per 
l’assegnazione dei garanti ai corsi universitari, in conformità ai requisiti ministeriali. 
L’obiettivo principale è garantire che ogni corso soddisfi i vincoli minimi di docenza, 
rispettando le regole di distribuzione tra diverse categorie di docenti e ottimizzando 
l’uso delle risorse disponibili.

Utilizzando la programmazione logica con Answer Set Programming (ASP), 
abbiamo modellato il problema attraverso fatti, regole e vincoli derivati dai dati 
ministeriali e universitari. Abbiamo implementato una serie di vincoli per rispettare 
i minimi richiesti di docenti per corso, evitando sovrapposizioni improprie tra gli 
incarichi dei docenti e considerando scenari realistici in cui un docente può assumere 
più ruoli parziali.

L’approccio è stato testato su un dataset reale contenente informazioni su corsi, SSD 
(Settori Scientifico-Disciplinari) e docenti dell'Università degli Studi di Parma. 
I risultati dimostrano come il sistema possa trovare configurazioni ottimali che 
soddisfano i requisiti, massimizzando l’efficienza e mantenendo flessibilità 
nell’assegnazione dei docenti.

## Requisiti per l'utilizzo
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
