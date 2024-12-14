# Come replicare i risultati della valutazione della soluzione proposta
La valutazione della soluzione proposta è stata effettuata utilizzando tre dataset distinti, ciascuno corrispondente a una specifica configurazione dei corsi. I dataset, organizzati nelle cartelle `lp-dataset-1`, `lp-dataset-2` e `lp-dataset-3`, contengono i fatti ASP generati per i benchmark. 

## Dataset 1: Esempio Giocattolo
Il primo dataset (`lp-dataset-1`) rappresenta un esempio giocattolo basato sui corsi di laurea in Informatica (LT) e Scienze Informatiche (LM). Questo dataset è stato progettato per testare la capacità del modello di rispettare i vincoli e ottimizzare le soluzioni in un contesto semplificato. 

Comando per lanciare l'analisi:
```bash
clingo -n 15 lp-dataset-1/* main.lp
```

## Dataset 2: Dipartimento SMFI
Il secondo dataset (`lp-dataset-2`) include un insieme ridotto di corsi appartenenti al Dipartimento di Scienze Matematiche, Fisiche e Informatiche (SMFI). Questo dataset è stato utilizzato per valutare la scalabilità del modello e la sua capacità di gestire un numero maggiore di corsi rispetto all'esempio giocattolo.

Comando per lanciare l'analisi:
```bash
clingo -n 15 --parallel-mode 10 --time-limit=180 lp-dataset-2/* main.lp
```

## Dataset 3: Tutti i Corsi del Dipartimento
Il terzo dataset (`lp-dataset-3`) comprende tutti i corsi di studio del dipartimento, rappresentando il caso più complesso tra i tre. 
Comando per lanciare l'analisi:
```bash
clingo -n 15 --parallel-mode 10 --time-limit=3600 lp-dataset-3/* main.lp
```