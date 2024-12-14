% Predicati di base per definire i pesi possibili.
% In questo caso, i pesi disponibili sono 5 e 10.
% peso(5).
peso(10).

% Assegna i docenti come garanti di un corso, specificando il peso e la fascia del docente.
% Questa regola si applica ai docenti a tempo indeterminato ('ti').
garante(Docente, Corso, Peso, Fascia) :- 
      cattedra(Corso, Docente, _, _),
      peso(Peso),
      docente(Docente, Fascia, _, _),
      fascia(Fascia),
      Fascia = ti,
      Docente = #min {D : cattedra(Corso, D, _, _)}.

% Assegna i docenti come garanti di un corso, specificando il peso e la fascia del docente.
% Questa regola si applica ai docenti a tempo determinato ('td').
garante(Docente, Corso, Peso, Fascia) :- 
      cattedra(Corso, Docente, _, _),
      peso(Peso),
      docente(Docente, Fascia, _, _),
      fascia(Fascia),
      Fascia = td,
      Docente = #min {D : cattedra(Corso, D, _, _)}.

% Determina il numero minimo e massimo di docenti a tempo indeterminato assegnabili come garanti per un corso.
% L'aggregato considera i docenti nella fascia 'ti' (tempo indeterminato) associati al corso,
% ordinandoli in base alla loro matricola. Sono incluse verifiche per evitare la duplicazione di docenti.
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


% Determina il numero massimo di docenti a tempo determinato assegnabili come garanti per un corso.
% L'aggregato considera i docenti nella fascia 'td' (tempo determinato) associati al corso,
% ordinandoli in base alla loro matricola. Sono incluse verifiche per evitare la duplicazione di docenti.
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
