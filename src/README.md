# Come replicare i risultati della valutazione della soluzione proposta
La valutazione della soluzione proposta è stata effettuata utilizzando tre dataset distinti, ciascuno corrispondente a una specifica configurazione dei corsi. I dataset, organizzati nelle cartelle `lp-dataset-1`, `lp-dataset-2` e `lp-dataset-3`, contengono i fatti ASP generati per i benchmark.

## Dataset 1: Esempio Giocattolo
Il primo dataset (`lp-dataset-1`) rappresenta un esempio giocattolo basato sui corsi di laurea in Informatica (LT) e Scienze Informatiche (LM).

Comando per generare il dataset:
```bash
python3 main.py --3027 --5069
```

Comando per lanciare l'analisi:
```bash
clingo -n 0 --parallel-mode 9 benchmark/lp-dataset-1/* main.lp
```

## Dataset 2: Dipartimento SMFI
Il secondo dataset (`lp-dataset-2`) include un insieme ridotto di corsi appartenenti al Dipartimento di Scienze Matematiche, Fisiche e Informatiche (SMFI).

Comando per generare il dataset:
```bash
python3 main.py --3027 --5069 --3026 --5036 --3030 --5037
```

Comando per lanciare l'analisi:
```bash
clingo -n 0 --parallel-mode 9 --time-limit=3600 benchmark/lp-dataset-2/* main.lp
```

## Dataset 3: Tutti i Corsi del Dipartimento
Il terzo dataset (`lp-dataset-3`) comprende tutti i corsi di studio del dipartimento.

Comando per generare il dataset:
```bash
python3 main.py --all
```

Comando per lanciare l'analisi:
```bash
clingo -n 0 --parallel-mode 9 --time-limit=3600 benchmark/lp-dataset-3/* main.lp
```
