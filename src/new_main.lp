% Trova i possibili garanti per ogni corso e laurea
{garante(Docente, Corso) : cattedra(Corso, Docente, Laurea)} :-
    corso(Corso, Laurea, SSD, _),
    codice_corso(Corso),
    matricola_docente(Docente),
    laurea(Laurea).

% Evita che lo stesso docente sia garante di più corsi
:- garante(Docente, Corso1), 
   garante(Docente, Corso2), 
   Corso1 != Corso2,
   matricola_docente(Docente),
   codice_corso(Corso1), 
   codice_corso(Corso2).

% Associa il minimo ministeriale a ogni corso
ministeriale(Corso, Minimo) :-
    corso(Corso, Laurea, _, _),
    minimo_ministeriale(Laurea, Minimo).

% Vincolo: il numero di garanti scelti per ciascun corso deve rispettare il minimo ministeriale
numero_garanti_corso(Corso, Minimo, Realta) :- ministeriale(Corso, Minimo),
   Realta = #count{Docente : garante(Docente, Corso)} < Minimo.

% Vincolo: un docente può essere garante di un solo corso
:- garante(Docente, Corso1),
   garante(Docente, Corso2),
   Corso1 != Corso2.

% Mostra i risultati
% #show garante/2.
% #show ministeriale/2.
#show numero_garanti_corso/3.