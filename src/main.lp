% Predicati di base per definire i pesi possibili.
% In questo caso, i pesi disponibili sono 5 e 10.
% peso(5).
peso(10).

% Generazione dei garanti non a contratto come possibili garanti.
% Questa regola considera i docenti appartenenti alle fasce 'td' (tempo determinato) 
% e 'ti' (tempo indeterminato) per l'assegnazione come garanti di un corso. 
% I docenti a contratto (fascia 'c') sono esclusi dal predicato tramite la condizione `Fascia != c`.
%
% Il numero minimo di garanti è calcolato sottraendo dal minimo complessivo richiesto per il corso 
% (MinimoComplessivo) il numero massimo di docenti a contratto consentiti (MassimoDocentiContratto).
% Il numero massimo di garanti non a contratto coincide con il minimo complessivo richiesto per il corso 
% (MinimoComplessivo).
%
% Esempio:
% Per un corso con un minimo complessivo di 9 garanti e un massimo di 2 docenti a contratto:
% - Minimo garanti non a contratto = 9 - 2 = 7
% - Massimo garanti non a contratto = 9
Minimo{
      garante(Docente, Corso, Peso, Fascia) :
            cattedra(Corso, Docente, _, _),
            peso(Peso),
            docente(Docente, Fascia, _),
            fascia(Fascia),
            Fascia != c % Non serve perche' docente/4 usa solo fascie del tipo 'td' e 'ti' 
}Massimo :-
      ministeriale(Corso, MinimoComplessivo, _, _, MassimoDocentiContratto),
      Minimo = MinimoComplessivo - MassimoDocentiContratto,
      Massimo = MinimoComplessivo.

% Generazione dei docenti a contratto come possibili garanti.
% Questa regola considera i docenti indicati come 'jolly', ovvero quelli che 
% possono essere assegnati come garanti a qualsiasi corso, indipendentemente dal settore.
% I docenti a contratto sono rappresentati con la fascia 'c'.
% Il numero massimo di docenti a contratto è limitato dalla regola ministeriale associata al corso.
{     
      garante(Docente, Corso, 10, c) :
            jolly(Docente),
            codice_corso(Corso),
            peso(10),

            jolly(Docente2),
            codice_corso(Corso),
            peso(10),

            Docente > Docente2

}MassimoDocentiContratto :- ministeriale(Corso, _, _, _, MassimoDocentiContratto).

% Calcola il numero di docenti a tempo indeterminato assegnati come garanti a un determinato corso.
% Il numero è calcolato sommando i pesi di tutti i docenti nella fascia 'ti' associati al corso 
% e dividendo il risultato per 10.
conta_garanti_indeterminato(Corso, NumeroGaranti) :- 
      Numero = #sum { Peso, Docente : garante(Docente, Corso, Peso, ti)},
      codice_corso(Corso),
      NumeroGaranti = Numero / 10.

% Calcola il numero di docenti a tempo determinato assegnati come garanti a un determinato corso.
% Il numero è calcolato sommando i pesi di tutti i docenti nella fascia 'td' associati al corso 
% e dividendo il risultato per 10.
conta_garanti_determinato(Corso, NumeroGaranti) :- 
      Numero = #sum { Peso, Docente : garante(Docente, Corso, Peso, td)},
      codice_corso(Corso),
      NumeroGaranti = Numero / 10.

% Vincolo: il numero di docenti a tempo indeterminato per un corso deve essere almeno pari
% al minimo richiesto dalla normativa ministeriale per quel corso. Se non soddisfatto, 
% la soluzione viene scartata.
:- conta_garanti_indeterminato(Corso, Numero),
      ministeriale(Corso, _, Minimo_ind, _, _),
      Numero < Minimo_ind.

% Vincolo: il numero di docenti a tempo determinato per un corso non deve superare
% il massimo consentito dalla normativa ministeriale per quel corso. Se superato,
% la soluzione viene scartata.
:- conta_garanti_determinato(Corso, Numero),
      ministeriale(Corso, _, _, Massimo_det, _),
      Numero > Massimo_det.

% Calcola la somma totale dei pesi assegnati ai docenti per ciascun corso.
% La somma è ottenuta considerando i pesi di tutti i garanti (docenti) associati al corso.
% Questo predicato è utilizzato per verificare il rispetto dei vincoli di somma e multipli.
somma_pesi_corso(Corso, Somma) :-
      codice_corso(Corso),
      Somma = #sum{
            Peso, Docente : garante(Docente, Corso, Peso, _)
      }.

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
:- garante(Docente, Corso1, Peso1, Fascia),
      garante(Docente, Corso2, Peso2, Fascia),
      matricola_docente(Docente),
      codice_corso(Corso1), codice_corso(Corso2),
      Somma = Peso1 + Peso2,
      Somma > 10,
      peso(Peso1),
      peso(Peso2),
      Corso1 != Corso2,
      Fascia != c.

% Regola che esclude i docenti che sono associati allo stesso corso con pesi differenti.
% Se un docente ha pesi diversi per lo stesso corso e la loro somma è maggiore di 10, tale assegnazione viene esclusa.
:- garante(Docente, Corso1, Peso1, Fascia),
      garante(Docente, Corso1, Peso2, Fascia),
      matricola_docente(Docente),
      codice_corso(Corso1),
      Somma = Peso1 + Peso2,
      Somma > 10,
      peso(Peso1),
      peso(Peso2),
      Peso1 != Peso2,
      Fascia != c.

% Calcola il numero di garanti che afferiscono al settore scientifico-disciplinare (SSD) del corso.
% Il numero è calcolato sommando i pesi dei docenti garanti che afferiscono al SSD del corso
% e dividendo il risultato per 10.
numero_garanti_che_afferiscono(Numero, Corso) :- 
      SommaPesi = #sum {
            Peso ,Docente : garante(Docente, Corso, Peso, _),
                        docente(Docente, _, SettoreSSD),
                        corso(Corso, _, SettoreSSD)
      },
      codice_corso(Corso),
      Numero = SommaPesi / 10.

% Calcola il numero totale di docenti di riferimento assegnati a un corso.
% Esclude i docenti a contratto (fascia 'c') e conta il numero di docenti in altre fasce
% che sono assegnati al corso.
numero_garanti_di_riferimento(Numero, Corso) :- 
      codice_corso(Corso),
      Numero = #count {Docente : garante(Docente, Corso, _, Fascia), Fascia != c }.
      

% Vincolo: il numero di garanti che afferiscono al settore scientifico-disciplinare (SSD)
% di un corso deve essere almeno pari alla metà del numero totale di docenti di riferimento
% assegnati al corso. Se non soddisfatto, la soluzione viene scartata.
:- numero_garanti_che_afferiscono(Aff, Corso), 
      numero_garanti_di_riferimento(Tot, Corso),
      2 * Aff <= Tot. 

% Calcola il numero di docenti a contratto assegnati a ciascun corso.
% Questo predicato è utilizzato per verificare che il numero massimo di docenti
% a contratto non superi il valore specificato dalla regola ministeriale.
jolly_per_corso(Corso, Numero) :- 
      codice_corso(Corso),
      Numero = #count { Docente : garante(Docente, Corso, _, c) }.

% Calcola il numero di garanti effettivi per ciascun corso.
% Il numero di garanti viene determinato dividendo la somma totale
% dei pesi assegnati ai garanti per il corso (somma_pesi_corso)
% per 10.
garanti_per_corso(Corso, Numero) :-
      codice_corso(Corso),
      somma_pesi_corso(Corso, Somma),
      Numero = Somma / 10.

% Vincolo: il numero totale di garanti assegnati a un corso deve essere uguale
% al minimo richiesto dalla normativa ministeriale per quel corso. Se non soddisfatto,
% la soluzione viene scartata.
:- garanti_per_corso(Corso, Numero),
      ministeriale(Corso, Minimo, _, _, _),
      Numero != Minimo.

% Vincolo: il numero di docenti a contratto per ciascun corso non deve superare
% il valore massimo specificato dalla regola ministeriale.
% Se il numero di docenti a contratto assegnati supera il massimo consentito, la soluzione viene scartata.
:- jolly_per_corso(Corso, Numero),
      corso(Corso, Laurea, _),
      ministeriale(Corso, _, _, _, Massimo_numero_docenti_a_contratto),
      Numero > Massimo_numero_docenti_a_contratto.

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
#minimize { 100, Docente : garante(Docente, _, Peso, _), Peso = 5 }.
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
                  docente(Docente, _, SettoreSSD), 
                  corso(Corso, _, SettoreSSD) }.

% Minimizzo il numero di garanti per ogni corso
#minimize { Penalita : garanti_per_corso(Corso, Numero), Penalita = Numero * 10 }.

%%%%%%%%%%%%%%%%%%%%%%%%%%%% ! Show
% #show garanti_per_corso/2.
% #show jolly_per_corso/2.
% #show numero_garanti_che_afferiscono/2.
% #show numero_garanti_di_riferimento/2.
% #show somma_pesi_corso/2.
% #show conta_garanti_determinato/2.
% #show conta_garanti_indeterminato/2.
#show garante/4.