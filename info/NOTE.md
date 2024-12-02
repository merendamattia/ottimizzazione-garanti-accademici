# Primo punto sotto la tabella

Un docente è garante perché ha un insegnamento in quel corso.
Un docente può insegnare in due corsi differenti, a patto che sia garante al 50% in ogni corso insegnato. Il 50% restante può essere tappato da un altro professore che è garante al 50% in quel corso.

> Si preferisce il primo caso (quindi dobbiamo gestire le priorità).

# Preferenze

1. L'obbiettivo è avere il minor numero di garanti.
2. Minimizzare il numero di contratti.
3. Attualmente dobbiamo visualizzare una soluzione senza docenti a contratto.

# Dati inutili

1. CFU ed ORE non ci servono.
2. Se la matricola del docente non è nel file docenti.xlsx, allora non è un candidato ad essere garante. Quindi "scarto" la riga.

# Dati di interesse

| file           | colonne    |
| -------------- | ---------- |
| docenti.xlsx   | A, B, C, G |
| coperture.xlsx | C, G, H    |

# I docenti che possono essere considerati garanti

Tutti i docenti contenuti nel file `docenti.xlsx` sono candidati ottimali.

# Docenti a contratto

Un docente è a contratto se ha la cella della colonna D (i.e., "cod. settore docente") non valorizzata.

# Incoerenze

Sfruttare SSD per la separazione dei professori/corsi per dipartimenti non è corretta, vedi `m-psi_07`:

```csv
Cognome,Nome,Matricola,Cod. Settore Docente,Dipartimento Docente,Dipartimento carico didattico,Cod. Tipo Corso,Cod. Corso di Studio,Des. Corso di Studio,Cod. Att. Form.,Des. Insegnamento,SSD,TAF,CFU,Ore
DE PANFILIS,Chiara,102887.0,MEDS-11/A,Dipartimento di Medicina e Chirurgia,Dipartimento di Medicina e Chirurgia,LM,5053.0,PSICOBIOLOGIA E NEUROSCIENZE COGNITIVE,1011745,CLINICA DEI DISTURBI DELLA PERSONALITA',M-PSI/07,B,6.0,48.0
MUSETTI,Alessandro,10813.0,PSIC-04/A,"Dipartimento di Discipline Umanistiche, Sociali e delle Imprese Culturali",Dipartimento di Medicina e Chirurgia,L,3021.0,SCIENZE E TECNICHE PSICOLOGICHE,02505,PSICOLOGIA DINAMICA,M-PSI/07,B,6.0,42.0
MUSETTI,Alessandro,10813.0,PSIC-04/A,"Dipartimento di Discipline Umanistiche, Sociali e delle Imprese Culturali","Dipartimento di Discipline Umanistiche, Sociali e delle Imprese Culturali",LM,5054.0,PSICOLOGIA DELL'INTERVENTO CLINICO E SOCIALE,1009413,FONDAMENTI E METODI DELL'INTERVENTO PSICOLOGICO,M-PSI/07,B,3.0,21.0
MUSETTI,Alessandro,10813.0,PSIC-04/A,"Dipartimento di Discipline Umanistiche, Sociali e delle Imprese Culturali","Dipartimento di Discipline Umanistiche, Sociali e delle Imprese Culturali",LM,5054.0,PSICOLOGIA DELL'INTERVENTO CLINICO E SOCIALE,1008588,MODELLI CLINICO-DINAMICI DI INTERVENTO,M-PSI/07,B,6.0,42.0
nan,nan,nan,nan,nan,"Dipartimento di Discipline Umanistiche, Sociali e delle Imprese Culturali",LM,5054.0,PSICOLOGIA DELL'INTERVENTO CLINICO E SOCIALE,1009413,FONDAMENTI E METODI DELL'INTERVENTO PSICOLOGICO,M-PSI/07,B,3.0,21.0
```

## Righe vuote

Le righe vuote devono essere ignorate.

## Atomi/termini

| Colonna         | Fatto               | Esempio                                                                                              |
| --------------- | ------------------- | ---------------------------------------------------------------------------------------------------- |
| Cod. tipo corso | laurea/1            | laurea(l)                                                                                            |
| SSD             | ssd/2               | ssd(inf, 1)                                                                                          |
| Matricola       | matricola_docente/1 | matricola_docente(32990)                                                                             |
| Fascia          | fascia/1            | fascia(ti)                                                                                           |
| -               | docente/3           | docente(32990, ti, inf, 1) :- matricola_docente(32990), fascia(ti), ssd(inf, 1)                      |
| Cod. Corso      | codice_corso/1      | codice_corso(3023)                                                                                   |
| -               | corso/2             | corso(3023, l) :- codice_corso(3023), laurea(l)                                                      |
| -               | cattedra/3          | cattedra(32990, 3023, l) :- matricola_docente(32990), corso(3023,l), laurea(l)                       |
| -               | min_garanti/3       | min_garanti(l, 9, 5) :- laurea(l).                                                                   |
| -               | min_garanti_corso/3 | min_garanti_corso(3023, 9, 5) :- corso(3023, l), laurea(l), codice_corso(3023), min_garanti(l, 9, 5) |
