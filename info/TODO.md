# TODO

1. ✅ Modificare bilanciamento dei ricercatori (devono essere al piu' il numero che c'e' scritto in tabella)
2. ✅ Maximize ricercatori (piu' ce ne sono come garanti e meglio e')
3. ✅ Bisogna ottimizzare i garanti con il proprio ssd caratterizzante (Maximize)
4. Maximize: i presidenti di un corso devono essere preferibilmente garanti di quel corso (non sappiamo chi sono i presidenti del corso).
5. ✅ Riorganizzare le priorita' dei docenti scelti: TD > TI > C > peso(10) > peso(5)
6. Rimuovere la regola ministeriale/5 dal .lp e costruire i fatti relativi ad ogni corso nella fase di preprocessing (modificare la numerosita' per ogni corso di laurea con la formula della W) (pagina 20 https://www.unipr.it/sites/default/files/2024-02/Note%20procedurali%20per%20compilazione%20SUA-CdS%202024-25.pdf)
7. Tenere traccia anche del TAF per l'assegnamento dei garanti e andare a dare una priorita' maggiore ai possibili garanti che hanno come valore A e B (A > B > resto)

Lavori futuri:
1. Dovremo gestire i corsi a distanza.
2. Dovremo gestire i casi particolari di corsi inter-ateneo (tipo 5070 e 5057), dovrebbero essere solo due, e in questo caso diminuiscono i garanti in base ad un coefficiente
