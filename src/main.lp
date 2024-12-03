% Predicati di base per definire i pesi possibili.
% In questo caso, i pesi disponibili sono 5 e 10.
peso(5).
peso(10).

% Regola per associare il minimo ministeriale a ciascun corso.
% La regola assegna il valore minimo ministeriale a ogni corso in base al tipo di laurea.
ministeriale(Corso, Minimo, Minimo_ind, Minimo_det) :-
      corso(Corso, Laurea, _, _),
      minimo_ministeriale(Laurea, Minimo, Minimo_ind, Minimo_det).

% La regola 'minimo{garante/3}' associa ogni docente a un corso con un peso.
% La regola garantisce che ogni corso sia associato ad un docente con un peso definito.
% Il peso è assegnato in base alla relazione 'peso/1', che contiene i valori 5 e 10.
% Inoltre, il minimo ministeriale associato al corso viene rispettato.
Minimo{
            garante(Docente, Corso, Peso) :
            cattedra(Corso, Docente, _),
            peso(Peso)
      } :-
            ministeriale(Corso, Minimo, _, _).

% Conta il numero di docenti a tempo indeterminato associati a ciascun corso.
% La regola utilizza il predicato `cattedra/3` per identificare i docenti e verifica che appartengano alla fascia "ti" (tempo indeterminato).
conta_docenti_indeterminato(Corso, Numero) :- 
      Numero = #count { 1, Docente : cattedra(Corso, Docente, _), docente(Docente, Fascia, _, _)},
      Fascia = ti,
      codice_corso(Corso).

% Conta il numero di docenti a tempo determinato associati a ciascun corso.
% La regola utilizza il predicato `cattedra/3` per identificare i docenti e verifica che appartengano alla fascia "td" (tempo determinato).
conta_docenti_determinato(Corso, Numero) :- 
      Numero = #count { 1, Docente : cattedra(Corso, Docente, _), docente(Docente, Fascia, _, _)},
      Fascia = td,
      codice_corso(Corso).

% Vincolo: il numero di docenti a tempo indeterminato per ogni corso deve essere almeno pari al minimo ministeriale richiesto.
% Se il numero è inferiore al minimo, la soluzione viene scartata.
:- conta_docenti_indeterminato(Corso, Numero),
      ministeriale(Corso, Minimo, Minimo_ind, _),
      codice_corso(Corso),
      Numero < Minimo_ind.

% Vincolo: il numero di docenti a tempo determinato per ogni corso deve essere almeno pari al minimo ministeriale richiesto.
% Se il numero è inferiore al minimo, la soluzione viene scartata.
:- conta_docenti_determinato(Corso, Numero),
      ministeriale(Corso, Minimo, _, Minimo_det),
      codice_corso(Corso),
      Numero < Minimo_det.

% Calcola la somma totale dei pesi assegnati ai docenti per ciascun corso.
% La somma è ottenuta considerando i pesi di tutti i garanti (docenti) associati al corso.
% Questo predicato è utilizzato per verificare il rispetto dei vincoli di somma e multipli.
somma_pesi_corso(Corso, Somma) :-
      codice_corso(Corso),
      Somma = #sum{
            Peso, Docente : garante(Docente, Corso, Peso)
      }.

% Vincolo: la somma totale dei pesi deve essere almeno 10 volte il minimo ministeriale del corso.
% Questo assicura che il numero complessivo di garanti sia sufficiente per soddisfare i requisiti ministeriali.
:- somma_pesi_corso(Corso, Somma),
      ministeriale(Corso, Minimo, _, _),
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
:- garante(Docente, Corso1, Peso1),
      garante(Docente, Corso2, Peso2),
      matricola_docente(Docente),
      codice_corso(Corso1), codice_corso(Corso2),
      Somma = Peso1 + Peso2,
      Somma > 10,
      peso(Peso1),
      peso(Peso2),
      Corso1 != Corso2.

% Regola che esclude i docenti che sono associati allo stesso corso con pesi differenti.
% Se un docente ha pesi diversi per lo stesso corso e la loro somma è maggiore di 10, tale assegnazione viene esclusa.
:- garante(Docente, Corso1, Peso1),
      garante(Docente, Corso1, Peso2),
      matricola_docente(Docente),
      codice_corso(Corso1),
      Somma = Peso1 + Peso2,
      Somma > 10,
      peso(Peso1),
      peso(Peso2),
      Peso1 != Peso2.

% Priorità per i garanti con peso 10
#maximize{Peso : garante(_, _, Peso), Peso = 10}.

#show minimo_ministeriale/4.
#show somma_pesi_corso/2.
#show garante/3.
#show conta_docenti_indeterminato/2.
#show conta_docenti_determinato/2.