# Usare clingo con più file sorgenti contemporaneamente

I file che precedono il main devono contenere solo i fatti e le regole (i.e., il database).
Nel main aggiungiamo i vari vincoli.

```bash
clingo -n 15 --parallel-mode 8 --time-limit=180 lp/* main-ottimizzato.lp
```

Corsi di Informatica (LT e LM)

```bash
python3 main.py --3027 --5069
```

Dipartimento SMFI

```bash
python3 main.py --3027 --5069 --3026 --5036 --3030 --5037
```
