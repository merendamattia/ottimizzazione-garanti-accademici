% Predicati di base per definire i pesi possibili.
% In questo caso, i pesi disponibili sono 5 e 10.
peso(5).
peso(10).


% Regola per associare il minimo ministeriale a ciascun corso.
% La regola assegna il valore minimo ministeriale a ogni corso in base al tipo di laurea.
ministeriale(Corso, Minimo) :-
      corso(Corso, Laurea, _, _),
      minimo_ministeriale(Laurea, Minimo).


% La regola 'minimo{garante/3}' associa ogni docente a un corso con un peso.
% La regola garantisce che ogni corso sia associato ad un docente con un peso definito.
% Il peso è assegnato in base alla relazione 'peso/1', che contiene i valori 5 e 10.
% Inoltre, il minimo ministeriale associato al corso viene rispettato.
Minimo{garante(Docente, Corso, Peso) :
            cattedra(Corso, Docente, _),
            peso(Peso)
      } :-
            ministeriale(Corso, Minimo).

% {garante(Docente, Corso, Peso) : peso(Peso)} :-
%       cattedra(Corso, Docente, Laurea),
%       corso(Corso, Laurea, _, _).

% La somma di tutti i pesi devono essere esattamente 10 volte il minimo

somma_pesi_corso(Corso, Somma) :-
      codice_corso(Corso),
      Somma = #sum{
            Peso, Docente, Corso : garante(Docente, Corso, Peso)
      }.

:- somma_pesi_corso(Corso, Somma),
      minimo_ministeriale(Corso, Minimo),
      codice_corso(Corso),
      Min = 10 * Minimo,
      Somma < Min.

% :- Somma_pesi = #sum{
%       Peso : garante(Docente, Corso, Peso)
%       },
%       codice_corso(Corso),
%       Somma_pesi != 10*Minimo,
%       ministeriale(Corso, Minimo).


% un garante deve coprire esattamente 10


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
      

#show minimo_ministeriale/2.
#show somma_pesi_corso/2.
#show garante/3.