% Predicati di base per definire i pesi possibili.
% In questo caso, i pesi disponibili sono 5 e 10.
% peso(5).
peso(10).

garante(Docente, Corso, Peso, Fascia) :- 
      cattedra(Corso, Docente, _, _),
      peso(Peso),
      docente(Docente, Fascia, _, _),
      fascia(Fascia),
      Fascia = ti,
      Docente = #min {D : cattedra(Corso, D, _, _)}.

garante(Docente, Corso, Peso, Fascia) :- 
      cattedra(Corso, Docente, _, _),
      peso(Peso),
      docente(Docente, Fascia, _, _),
      fascia(Fascia),
      Fascia = td,
      Docente = #min {D : cattedra(Corso, D, _, _)}.

MinimoIndeterminato{
      garante(Docente, Corso, Peso, Fascia) :
            fascia(Fascia),
            Fascia = ti,
            
            % Docente 1
            cattedra(Corso, Docente, _, _),
            peso(Peso),
            docente(Docente, Fascia, _, _),
            
            % Docente 2
            cattedra(Corso, Docente2, _, _),
            peso(Peso),
            docente(Docente2, Fascia, _, _),

            Docente > Docente2

}Massimo :-
      ministeriale(Corso, MassimoIndeterminato, MinimoIndeterminato, _, _),
      Massimo = MassimoIndeterminato * 2.



{
      garante(Docente, Corso, Peso, Fascia) :
            fascia(Fascia),
            Fascia = td,
            
            % Docente 1
            cattedra(Corso, Docente, _, _),
            peso(Peso),
            docente(Docente, Fascia, _, _),
            
            % Docente 2
            cattedra(Corso, Docente2, _, _),
            peso(Peso),
            docente(Docente2, Fascia, _, _),

            Docente > Docente2

}Massimo :-
      ministeriale(Corso, _, _, MassimoDeterminato, _),
      Massimo = MassimoDeterminato * 2.




% Mostra i risultati.
#show garante/4.
