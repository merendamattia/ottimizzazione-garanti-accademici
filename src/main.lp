% Trovo i garanti
garante(Docente, Corso, SSD) :- docente_corso(Corso, Docente), 
                                corso(Corso, _, SSD), 
                                docente_ssd(Docente, SSD),
                                matricola_docente(Docente),
                                matricola_corso(Corso).
% #show garante/3.

% Conta il numero di garanti assegnati a un SSD
numero_garanti(Livello, SSD, N) :- ssd(SSD), 
                                laurea(Livello),
                                N = #count{Docente : garante(Corso, Docente, SSD)}.
#show numero_garanti/3.

% Vincolo: il numero di garanti non deve essere inferiore al minimo
:- min_garanti(Livello, SSD, Min), 
   numero_garanti(Livello, SSD, N), 
   N < Min.

% Massimizzare i docenti con SSD caratterizzanti
#maximize{1 : garante(Docente, Corso, SSD), 
                docente_ssd(Docente, SSD), 
                corso(Corso, _, SSD)}.
