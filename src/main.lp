% Predicati di base per definire i pesi possibili.
% In questo caso, i pesi disponibili sono 5 e 10.
peso(5).
peso(10).

% Generazione dei docenti non a contratto come possibili garanti.
% Questa regola considera solo i docenti appartenenti alle fasce 'td' (tempo determinato)
% e 'ti' (tempo indeterminato). I docenti a contratto ('c') sono esclusi tramite il controllo `Fascia != c`.
% Il numero minimo di docenti richiesto è specificato dalla regola ministeriale.
Minimo{
      garante(Docente, Corso, Peso, Fascia) :
            cattedra(Corso, Docente, _, _),
            peso(Peso),
            docente(Docente, Fascia, _, _),
            fascia(Fascia),
            Fascia != c % Non serve perche' docente/4 usa solo fascie del tipo 'td' e 'ti' 
      } :-
            ministeriale(Corso, Minimo, _, _, _).

% Generazione dei docenti a contratto come possibili garanti.
% Questa regola considera i docenti indicati come 'jolly', ovvero quelli che 
% possono essere assegnati come garanti a qualsiasi corso, indipendentemente dal settore.
% I docenti a contratto sono rappresentati con la fascia 'c'.
% Il numero massimo di docenti a contratto è limitato dalla regola ministeriale associata al corso.
{     
      garante(Docente, Corso, Peso, c) :
            jolly(Docente),
            codice_corso(Corso),
            peso(Peso)
}Massimo :- ministeriale(Corso, _, _, _, Massimo).

#show garante/4.

% Conta il numero di docenti a tempo indeterminato associati a ciascun corso.
% La regola utilizza il predicato `cattedra/4` per identificare i docenti e verifica che appartengano alla fascia "ti" (tempo indeterminato).
conta_docenti_indeterminato(Corso, Numero) :- 
      Numero = #count { 1, Docente : cattedra(Corso, Docente, _, _), docente(Docente, Fascia, _, _)},
      Fascia = ti,
      codice_corso(Corso).

#show conta_docenti_indeterminato/2.

% Conta il numero di docenti a tempo determinato associati a ciascun corso.
% La regola utilizza il predicato `cattedra/4` per identificare i docenti e verifica che appartengano alla fascia "td" (tempo determinato).
conta_docenti_determinato(Corso, Numero) :- 
      Numero = #count { 1, Docente : cattedra(Corso, Docente, _, _), docente(Docente, Fascia, _, _)},
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
      [Numero * 10@1]

% Vincolo: il numero di docenti a tempo determinato per ogni corso non deve essere superiore al massimo ministeriale richiesto.
% Se il numero è superiore al massismo, la soluzione viene scartata.
% Penalizzazione per ricercatori che superano il limite consentito
% ! weak constraint
:~ conta_docenti_determinato(Corso, Numero),
      ministeriale(Corso, _, _, Massimo_det, _),
      Numero > Massimo_det,
      Penalita = Numero - Massimo_det.
      [Penalita * 50@1]

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
      [Tot - 4 * Aff@1]

#show numero_docenti_di_riferimento/1.

% Calcola il numero di docenti a contratto assegnati a ciascun corso.
% Questo predicato è utilizzato per verificare che il numero massimo di docenti
% a contratto non superi il valore specificato dalla regola ministeriale.
jolly_per_corso(Corso, Numero) :- 
      codice_corso(Corso),
      Numero = #count { Docente : garante(Docente, Corso, _, c) }.

#show jolly_per_corso/2.

% Calcola il numero di garanti effettivi per ciascun corso.
% Il numero di garanti viene determinato dividendo la somma totale
% dei pesi assegnati ai garanti per il corso (somma_pesi_corso)
% per 10.
garanti_per_corso(Corso, Numero) :-
      codice_corso(Corso),
      somma_pesi_corso(Corso, Somma),
      Numero = Somma / 10.

#show garanti_per_corso/2.

% Vincolo: il numero di docenti a contratto per ciascun corso non deve superare
% il valore massimo specificato dalla regola ministeriale.
% Se il numero di docenti a contratto assegnati supera il massimo consentito, la soluzione viene scartata.
:- jolly_per_corso(Corso, Numero),
      corso(Corso, Laurea, _, _),
      ministeriale(Corso, _, _, _, Massimo_numero_docenti_a_contratto),
      Numero > Massimo_numero_docenti_a_contratto.
      %[10 * Numero@1]

%%%%%%%%%%%%%%%%%%%%%%%%%%%% ! Priorità generali
% Massimizzare i docenti a tempo determinato (ricercatori)
#maximize { 50 : garante(_, _, _, td) }.

% Massimizzare i docenti a tempo indeterminato
#maximize { 40 : garante(_, _, _, ti) }.

% Minimizzare i docenti a contratto
#maximize { 32 : garante(_, _, _, c) }.

% Massimizzare i docenti con peso 10
#maximize { 25 : garante(_, _, Peso, _), Peso = 10 }.

% Minimizzare i docenti con peso 5
#minimize { 100 : garante(_, _, Peso, _), Peso = 5 }.
%%%%%%%%%%%%%%%%%%%%%%%%%%%% ! 

%%%%%%%%%%%%%%%%%%%%%%%%%%%% ! Massimizzo i docenti con TAF maggiore
#maximize { 25 : garante(Docente, Corso, _, _), 
                  cattedra(Corso, Docente, _, TAF), 
                  TAF = a}.
#maximize { 18 : garante(Docente, Corso, _, _), 
                  cattedra(Corso, Docente, _, TAF), 
                  TAF = b}.
#maximize { 10 : garante(Docente, Corso, _, _), 
                  cattedra(Corso, Docente, _, TAF), 
                  TAF = c}.
%%%%%%%%%%%%%%%%%%%%%%%%%%%% ! 

% Ottimizzare i garanti con SSD caratterizzante
#maximize { 20 : garante(Docente, Corso, _, _), 
                  docente(Docente, _, SettoreSSD, _), 
                  corso(Corso, _, SettoreSSD, _) }.

% Minimizzo il numero di garanti per ogni corso
#minimize { Penalita : garanti_per_corso(Corso, Numero), Penalita = Numero * 10 }.