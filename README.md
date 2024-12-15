# Ottimizzazione dei Garanti accademici
Realizzato da:
- [Colli Simone](https://github.com/SimoneColli)
- [Merenda Saverio Mattia](https://github.com/merendamattia)

Questo lavoro presenta l'analisi e l'implementazione di un sistema automatizzato per 
l'assegnazione dei garanti ai corsi universitari, in conformità ai requisiti ministeriali. 
L'obiettivo principale è garantire che ogni corso soddisfi i vincoli minimi di docenza, 
rispettando le regole di distribuzione tra diverse categorie di docenti e ottimizzando 
l'uso delle risorse disponibili.

Utilizzando la programmazione logica con Answer Set Programming (ASP), 
abbiamo modellato il problema attraverso fatti, regole e vincoli derivati dai dati 
ministeriali e universitari. Abbiamo implementato una serie di vincoli per rispettare 
i minimi richiesti di docenti per corso, evitando sovrapposizioni improprie tra gli 
incarichi dei docenti e considerando scenari realistici in cui un docente può assumere 
più ruoli parziali.

L'approccio è stato testato su un dataset reale contenente informazioni su corsi, SSD 
(Settori Scientifico-Disciplinari) e docenti dell'Università degli Studi di Parma. 
I risultati dimostrano come il sistema possa trovare configurazioni ottimali che 
soddisfano i requisiti, massimizzando l'efficienza e mantenendo flessibilità 
nell'assegnazione dei docenti.

## Requisiti per l'utilizzo
Per utilizzare il sistema, è necessario avere i seguenti strumenti installati:
-   [Docker](https://docs.docker.com/engine/install/)
-   [Docker Compose](https://docs.docker.com/compose/install/)

Verifica l'installazione con i seguenti comandi:
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
docker compose run --rm ottimizzazione-garanti-accademici
```

> Potrebbe essere necessario aggiornare i permessi della cartella `src` con `chmod -R 777 src`.

## Generazione del Dataset LP
Il sistema consente di generare dataset ASP per i corsi universitari attraverso uno script Python eseguito all'interno del container Docker. È possibile visualizzare l'helper per i comandi disponibili con:
```bash
python3 main.py --help
```

Per generare un dataset specifico (ad esempio per i corsi di Informatica e Scienze Informatiche):
```bash
python3 main.py --3027 --5069
```

I file generati verranno salvati nella directory `lp/` con i seguenti nomi:
- `docenti.lp`: contiene i fatti relativi ai docenti.
- `coperture.lp`: contiene i fatti relativi alle coperture dei corsi.
- `docenti_a_contratto.lp`: contiene i fatti relativi ai docenti a contratto.
- `ministeriali.lp`: contiene i vincoli ministeriali per i corsi.

## Analisi del Dataset
Per analizzare un dataset generato:
```bash
clingo -n 15 --parallel-mode 8 --time-limit=180 lp/* main.lp
```

---

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
