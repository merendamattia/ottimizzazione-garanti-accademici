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

## Righe vuote

Le righe vuote devono essere ignorate.

## Atomi/termini

| Colonna         | Fatto                  | Esempio                                                                                              |
| --------------- | ---------------------- | ---------------------------------------------------------------------------------------------------- |
| Cod. tipo corso | laurea/1               | laurea(l)                                                                                            |
| SSD             | ssd/2                  | ssd(inf, 1)                                                                                          |
| Matricola       | matricola_docente/1    | matricola_docente(32990)                                                                             |
| Fascia          | fascia/1               | fascia(ti)                                                                                           |
| -               | docente/4              | docente(32990, ti, inf, 1) :- matricola_docente(32990), fascia(ti), ssd(inf, 1)                      |
| Cod. Corso      | codice_corso/1         | codice_corso(3023)                                                                                   |
| -               | corso/4                | corso(3023, l, inf, 1) :- codice_corso(3023), laurea(l), ssd(inf, 1)                                 |
| -               | cattedra/3             | cattedra(32990, 3023, l) :- matricola_docente(32990), corso(3023,l), laurea(l)                       |
| -               | minimo_ministeriale/4  | minimo_ministeriale(lt, 9, 5, 4) :- laurea(lt).                                                      |
