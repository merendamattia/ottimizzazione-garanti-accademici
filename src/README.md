# Usare clingo con più file sorgenti contemporaneamente

I file che precedono il main devono contenere solo i fatti e le regole (i.e., il database). 
Nel main aggiungiamo i vari vincoli.
```bash
clingo lp/informatica.lp main.lp
```