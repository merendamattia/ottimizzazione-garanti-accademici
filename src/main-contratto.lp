% Predicati di base per definire i pesi possibili.
% In questo caso, i pesi disponibili sono 5 e 10.
peso(5).
peso(10).

% Regola per associare il minimo ministeriale a ciascun corso.
% La regola assegna il valore minimo ministeriale a ogni corso in base al tipo di laurea.
ministeriale(Corso, Minimo, Minimo_ind, Minimo_det, Massimo_numero_docenti_a_contratto) :-
      corso(Corso, Laurea, _, _),
      minimo_ministeriale(Laurea, Minimo, Minimo_ind, Minimo_det, Massimo_numero_docenti_a_contratto).

#show minimo_ministeriale/5.

% TODO documentazione
% Docenti non a contratto come possibili garanti
Minimo{
      garante(Docente, Corso, Peso, Fascia) :
            cattedra(Corso, Docente, _),
            peso(Peso),
            docente(Docente, Fascia, _, _),
            fascia(Fascia),
            Fascia != c % Non serve perche' docente/4 usa solo fascie del tipo 'td' e 'ti' 
      } :-
            ministeriale(Corso, Minimo, _, _, _).

% TODO documentazione
% Docenti a contratto come possibili garanti
{     
      garante(Docente, Corso, Peso, c) :
            jolly(Docente),
            codice_corso(Corso),
            peso(Peso)
}Massimo :- ministeriale(Corso, _, _, _, Massimo).

#show garante/4.

% Conta il numero di docenti a tempo indeterminato associati a ciascun corso.
% La regola utilizza il predicato `cattedra/3` per identificare i docenti e verifica che appartengano alla fascia "ti" (tempo indeterminato).
conta_docenti_indeterminato(Corso, Numero) :- 
      Numero = #count { 1, Docente : cattedra(Corso, Docente, _), docente(Docente, Fascia, _, _)},
      Fascia = ti,
      codice_corso(Corso).

#show conta_docenti_indeterminato/2.

% Conta il numero di docenti a tempo determinato associati a ciascun corso.
% La regola utilizza il predicato `cattedra/3` per identificare i docenti e verifica che appartengano alla fascia "td" (tempo determinato).
conta_docenti_determinato(Corso, Numero) :- 
      Numero = #count { 1, Docente : cattedra(Corso, Docente, _), docente(Docente, Fascia, _, _)},
      Fascia = td,
      codice_corso(Corso).

#show conta_docenti_determinato/2.

% Vincolo: il numero di docenti a tempo indeterminato per ogni corso deve essere almeno pari al minimo ministeriale richiesto.
% Se il numero è inferiore al minimo, la soluzione viene scartata.
% ! weak constraint
:~ conta_docenti_indeterminato(Corso, Numero),
      ministeriale(Corso, Minimo, Minimo_ind, _, _),
      codice_corso(Corso),
      Numero < Minimo_ind.
      [Numero * 10@2]

% Vincolo: il numero di docenti a tempo determinato per ogni corso deve essere almeno pari al minimo ministeriale richiesto.
% Se il numero è inferiore al minimo, la soluzione viene scartata.
% ! weak constraint
:~ conta_docenti_determinato(Corso, Numero),
      ministeriale(Corso, Minimo, _, Minimo_det, _),
      codice_corso(Corso),
      Numero < Minimo_det.
      [Numero * 10@2]

% Calcola la somma totale dei pesi assegnati ai docenti per ciascun corso.
% La somma è ottenuta considerando i pesi di tutti i garanti (docenti) associati al corso.
% Questo predicato è utilizzato per verificare il rispetto dei vincoli di somma e multipli.
somma_pesi_corso(Corso, Somma) :-
      codice_corso(Corso),
      Somma = #sum{
            Peso, Docente : garante(Docente, Corso, Peso, _)
      }.

#show somma_pesi_corso/2.

% Vincolo: la somma totale dei pesi deve essere almeno 10 volte il minimo ministeriale del corso.
% Questo assicura che il numero complessivo di garanti sia sufficiente per soddisfare i requisiti ministeriali.
:- somma_pesi_corso(Corso, Somma),
      ministeriale(Corso, Minimo, _, _, _),
      codice_corso(Corso),
      Min = 10 * Minimo,
      Somma < Min.

% Vincolo: la somma totale dei pesi per un corso deve essere un multiplo di 10.
% Questo vincolo garantisce che i pesi assegnati siano bilanciati, evitando frazionamenti non supportati.
:- somma_pesi_corso(Corso, Somma),
      codice_corso(Corso),
      Modulo = Somma \ 10, % Con questa condizione verifichiamo che siamo bilanciati quelli al 50%
      Modulo != 0.

% Regola che esclude i docenti che hanno più di una cattedra con pesi che superano 10.
% Se un docente è associato a più corsi con pesi che, sommati, superano 10, tale assegnazione viene esclusa.
% Il docente non può avere due assegnazioni con un peso complessivo superiore a 10.
:- garante(Docente, Corso1, Peso1, _),
      garante(Docente, Corso2, Peso2, _),
      matricola_docente(Docente),
      codice_corso(Corso1), codice_corso(Corso2),
      Somma = Peso1 + Peso2,
      Somma > 10,
      peso(Peso1),
      peso(Peso2),
      Corso1 != Corso2.

% Regola che esclude i docenti che sono associati allo stesso corso con pesi differenti.
% Se un docente ha pesi diversi per lo stesso corso e la loro somma è maggiore di 10, tale assegnazione viene esclusa.
:- garante(Docente, Corso1, Peso1, _),
      garante(Docente, Corso1, Peso2, _),
      matricola_docente(Docente),
      codice_corso(Corso1),
      Somma = Peso1 + Peso2,
      Somma > 10,
      peso(Peso1),
      peso(Peso2),
      Peso1 != Peso2.

% Calcola il numero di docenti che afferiscono al settore scientifico disciplinare (SSD) del corso.
% Un docente è considerato "afferente" se il suo SSD coincide con quello del corso per cui è garante.
% Il predicato utilizza la somma dei docenti e dei corsi per determinare il numero totale di afferenti.
numero_docenti_che_afferiscono(Numero) :- 
      Numero = #sum { 1, Docente, Corso : garante(Docente, Corso, _, _),
                                          docente(Docente, _, SettoreSSD, _),
                                          corso(Corso, _, SettoreSSD, _)
                  }.

#show numero_docenti_che_afferiscono/1.

% Calcola il numero totale di docenti di riferimento.
% Questo predicato considera tutti i docenti che sono garanti di uno o più corsi,
% indipendentemente dall'SSD o da altri criteri.
numero_docenti_di_riferimento(Numero) :- 
      Numero = #sum { 1, Docente, Corso : garante(Docente, Corso, _, _) }.

% Vincolo: il numero di docenti che afferiscono al SSD del corso deve rappresentare almeno il 50%
% del numero totale di docenti di riferimento.
% Se la condizione non è soddisfatta, la soluzione viene scartata.
% ! weak constraint
:~ numero_docenti_che_afferiscono(Aff), 
      numero_docenti_di_riferimento(Tot),
      2 * Aff <= Tot. 
      [Tot - 2 * Aff@1]

#show numero_docenti_di_riferimento/1.

jolly_per_corso(Corso, Numero) :- 
      codice_corso(Corso),
      Numero = #count { Docente : garante(Docente, Corso, _, c) }.

#show jolly_per_corso/2.

% TODO documentazione
:- jolly_per_corso(Corso, Numero),
      corso(Corso, Laurea, _, _),
      ministeriale(Corso, _, _, _, Massimo_numero_docenti_a_contratto),
      Numero > Massimo_numero_docenti_a_contratto.
      %[10 * Numero@1]

% Priorità per i garanti con peso 10
#maximize { Peso : garante(_, _, Peso, _), Peso = 10 }.

% TODO documentazione
% Do' un peso alto cosi viene 'penalizzato' molto
#minimize { 100 : garante(_, _, _, c) }. 
