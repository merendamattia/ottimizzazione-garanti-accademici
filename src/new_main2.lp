% Pesi validi per i garanti
peso(5).
peso(10).

% Associa il minimo ministeriale a ogni corso
ministeriale(Corso, Minimo) :-
    corso(Corso, Laurea, _, _),
    minimo_ministeriale(Laurea, Minimo).

% Generazione dei possibili garanti con peso
{garante(Docente, Corso, Peso) : peso(Peso)} :-
    cattedra(Corso, Docente, Laurea),
    corso(Corso, Laurea, _, _).

% Calcola il numero effettivo di garanti per ogni corso
numero_garanti_effettivi(Corso, N) :-
    codice_corso(Corso),
    N = #count{Docente : garante(Docente, Corso, _)}.

% Vincolo: il numero di garanti effettivi per ciascun corso deve essere maggiore o uguale al minimo ministeriale
:- ministeriale(Corso, Minimo),
   numero_garanti_effettivi(Corso, N),
   N < Minimo.

% Vincolo: un docente può contribuire al massimo al 100% su uno o più corsi
:- matricola_docente(Docente),
   #sum{Peso : garante(Docente, Corso, Peso)} > 10.

% Priorità per i garanti con peso 10
#maximize{Peso : garante(_, _, Peso), Peso = 10}.

% Mostra i risultati
#show numero_garanti_effettivi/2.
#show garante/3.