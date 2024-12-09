# Usare clingo con più file sorgenti contemporaneamente

I file che precedono il main devono contenere solo i fatti e le regole (i.e., il database).
Nel main aggiungiamo i vari vincoli.

```bash
clingo -n 15 --parallel-mode 8 --time-limit=180 lp/* main.lp
```
