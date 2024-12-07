# Sanitizzazione degli input

```bash
python3 sanitize.py
```

Lo script fa la sanitizzazione dei dataset in input. I dataset non sani sono:

-   `dataset/coperture.csv`
-   `dataset/docenti.csv`

I file sanitizzati sono:
-   `dataset/coperture_sanitized.csv`
-   `dataset/docenti_sanitized.csv`
-   
# Usare clingo con più file sorgenti contemporaneamente

I file che precedono il main devono contenere solo i fatti e le regole (i.e., il database).
Nel main aggiungiamo i vari vincoli.

```bash
clingo -n 5 --parallel-mode 8 --time-limit=120 lp/* main-contratto.lp
```
