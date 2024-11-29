
% Trovo i garanti potenziali
garante_potenziale(Docente, Corso, Laurea, SettoreSSD, NumeroSSD) :- 
      docente_corso(Corso, Docente), 
      corso(Corso, Laurea, SettoreSSD, NumeroSSD), 
      docente_ssd(Docente, SettoreSSD, NumeroSSD),
      matricola_docente(Docente),
      matricola_corso(Corso),
      laurea(Laurea).

% Decisione: scegliere un docente come garante
scelto_garante(Docente, Corso, Laurea) :- 
      garante_potenziale(Docente, Corso, Laurea, _, _).

% Conta i garanti scelti per ogni SSD
numero_garanti_scelti(Laurea, SettoreSSD, NumeroSSD, N) :- 
      ssd(SettoreSSD, NumeroSSD),
      laurea(Laurea), 
      N = #count{Docente : scelto_garante(Docente, Corso, Laurea), 
                           corso(Corso, Laurea, SettoreSSD, NumeroSSD)}.

% Vincolo: il numero di garanti scelti per ogni SSD deve rispettare il minimo richiesto
% :- min_garanti(Laurea, SettoreSSD, NumeroSSD, Min), 
%      numero_garanti_scelti(Laurea, SettoreSSD, NumeroSSD, N), 
%      N < Min.

% Vincolo: un docente può essere garante di un corso solo se è tra i potenziali
:- scelto_garante(Docente, Corso, Laurea), 
   not garante_potenziale(Docente, Corso, Laurea, _, _),
   laurea(Laurea).

% Minimizza il numero totale di garanti selezionati
% #minimize{1 : scelto_garante(Docente, Corso, Laurea)}.

% #show per debugging
#show scelto_garante/3.
#show numero_garanti_scelti/4.