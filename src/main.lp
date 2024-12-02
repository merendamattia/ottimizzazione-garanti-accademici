
%%%%%%%%%%%%%%%%%%%%%%%%% Vincoli ministeriali %%%%%%%%%%%%%%%%%%%%%%%%%

minimo_ministeriale(l, 9) :-
      laurea(l).

minimo_ministeriale(lm, 6) :-
      laurea(lm).

%minimo_ministeriale(lm5, 15) :-
%      laurea(lm5).

%minimo_ministeriale(lm6, 18) :-
%      laurea(lm6).


ministeriale(Corso, Laurea, Minimo) :-
      corso(Corso, Laurea, _, _),
      codice_corso(Corso),
      laurea(Laurea),
      minimo_ministeriale(Laurea, Minimo).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



%garante_potenziale(Docente, Corso) :-
%      cattedra(Corso, Docente, Laurea), 
%      ministeriale(Corso, Laurea, _),
%      laurea(Laurea).

%scelto_garante(Docente, Corso) :-
%      garante_potenziale(Docente, Corso).

%:- scelto_garante(Docente, Corso1),
%      not garante_potenziale(Docente, Corso2),
%      codice_corso(Corso1), codice_corso(Corso2),
%      Corso1 != Corso2,
%      matricola_docente(Docente).
%#show scelto_garante/2.

Minimo{garante(Docente, Corso) : cattedra(Docente, Corso, Laurea)}Minimo :-
%{garante(Docente, Corso) : cattedra(Docente, Corso, Laurea)} :-
ministeriale(Corso, Laurea, Minimo), laurea(Laurea).

:- garante(Docente, Corso1),
      garante(Docente, Corso2),
      matricola_docente(Docente),
      codice_corso(Corso1), codice_corso(Corso2),
      Corso1 != Corso2.

#show garante/2.