%  SEZIONE: Tipi di Corso
laurea(lt).
laurea(lm).

%  SEZIONE: SSD
ssd(inf).
ssd(mat).
ssd(chim).
ssd(fis).

%  SEZIONE: TAF
taf(b).
taf(a).
taf(c).

%  SEZIONE: Corsi
%  INFORMATICA (3027)
codice_corso(3027).
%  SCIENZE INFORMATICHE (5069)
codice_corso(5069).

%  SEZIONE: Informazioni Corsi
%  Corso: 3027 (lt)
corso(3027, lt, fis) :- codice_corso(3027), laurea(lt), ssd(fis).
%  Corso: 3027 (lt)
corso(3027, lt, inf) :- codice_corso(3027), laurea(lt), ssd(inf).
%  Corso: 3027 (lt)
corso(3027, lt, mat) :- codice_corso(3027), laurea(lt), ssd(mat).
%  Corso: 5069 (lm)
corso(5069, lm, inf) :- codice_corso(5069), laurea(lm), ssd(inf).

%  SEZIONE: Relazioni Corsi-Docenti
%  Corso: 3027, Docente: ARCERI Vincenzo
cattedra(3027, 33657, lt, b) :- codice_corso(3027), matricola_docente(33657), laurea(lt), taf(b).
%  Corso: 3027, Docente: ARCERI Vincenzo
cattedra(3027, 33657, lt, a) :- codice_corso(3027), matricola_docente(33657), laurea(lt), taf(a).
%  Corso: 3027, Docente: BAGNARA Roberto
cattedra(3027, 5145, lt, b) :- codice_corso(3027), matricola_docente(5145), laurea(lt), taf(b).
%  Corso: 5069, Docente: BAGNARA Roberto
cattedra(5069, 5145, lm, b) :- codice_corso(5069), matricola_docente(5145), laurea(lm), taf(b).
%  Corso: 3027, Docente: BENINI Anna
cattedra(3027, 26131, lt, a) :- codice_corso(3027), matricola_docente(26131), laurea(lt), taf(a).
%  Corso: 3027, Docente: BERGENTI Federico
cattedra(3027, 204741, lt, b) :- codice_corso(3027), matricola_docente(204741), laurea(lt), taf(b).
%  Corso: 5069, Docente: BERGENTI Federico
cattedra(5069, 204741, lm, b) :- codice_corso(5069), matricola_docente(204741), laurea(lm), taf(b).
%  Corso: 5069, Docente: BERGENTI Federico
cattedra(5069, 204741, lm, b) :- codice_corso(5069), matricola_docente(204741), laurea(lm), taf(b).
%  Corso: 3027, Docente: BERTINI FLAVIO
cattedra(3027, 32990, lt, b) :- codice_corso(3027), matricola_docente(32990), laurea(lt), taf(b).
%  Corso: 5069, Docente: BERTINI FLAVIO
cattedra(5069, 32990, lm, b) :- codice_corso(5069), matricola_docente(32990), laurea(lm), taf(b).
%  Corso: 3027, Docente: BONNICI Vincenzo
cattedra(3027, 34181, lt, b) :- codice_corso(3027), matricola_docente(34181), laurea(lt), taf(b).
%  Corso: 5069, Docente: BONNICI Vincenzo
cattedra(5069, 34181, lm, b) :- codice_corso(5069), matricola_docente(34181), laurea(lm), taf(b).
%  Corso: 3027, Docente: BONNICI Vincenzo
cattedra(3027, 34181, lt, b) :- codice_corso(3027), matricola_docente(34181), laurea(lt), taf(b).
%  Corso: 3027, Docente: BORGHESANI VALENTINA
cattedra(3027, 12129, lt, c) :- codice_corso(3027), matricola_docente(12129), laurea(lt), taf(c).
%  Corso: 5069, Docente: CHIESA Alessandro
cattedra(5069, 11047, lm, c) :- codice_corso(5069), matricola_docente(11047), laurea(lm), taf(c).
%  Corso: 3027, Docente: DAL PALU' Alessandro
cattedra(3027, 6625, lt, a) :- codice_corso(3027), matricola_docente(6625), laurea(lt), taf(a).
%  Corso: 5069, Docente: DAL PALU' Alessandro
cattedra(5069, 6625, lm, b) :- codice_corso(5069), matricola_docente(6625), laurea(lm), taf(b).
%  Corso: 3027, Docente: DAL PALU' Alessandro
cattedra(3027, 6625, lt, b) :- codice_corso(3027), matricola_docente(6625), laurea(lt), taf(b).
%  Corso: 3027, Docente: DE FILIPPIS Cristiana
cattedra(3027, 34499, lt, a) :- codice_corso(3027), matricola_docente(34499), laurea(lt), taf(a).
%  Corso: 3027, Docente: DE PIETRI Roberto
cattedra(3027, 5536, lt, a) :- codice_corso(3027), matricola_docente(5536), laurea(lt), taf(a).
%  Corso: 5069, Docente: DI RENZO Francesco
cattedra(5069, 5470, lm, c) :- codice_corso(5069), matricola_docente(5470), laurea(lm), taf(c).
%  Corso: 3027, Docente: GUARDASONI Chiara
cattedra(3027, 6801, lt, c) :- codice_corso(3027), matricola_docente(6801), laurea(lt), taf(c).
%  Corso: 5069, Docente: IOTTI ELEONORA
cattedra(5069, 13027, lm, b) :- codice_corso(5069), matricola_docente(13027), laurea(lm), taf(b).
%  Corso: 3027, Docente: IOTTI ELEONORA
cattedra(3027, 13027, lt, a) :- codice_corso(3027), matricola_docente(13027), laurea(lt), taf(a).
%  Corso: 5069, Docente: MORANDIN Francesco
cattedra(5069, 5804, lm, c) :- codice_corso(5069), matricola_docente(5804), laurea(lm), taf(c).
%  Corso: 3027, Docente: MUNARO Andrea
cattedra(3027, 36662, lt, b) :- codice_corso(3027), matricola_docente(36662), laurea(lt), taf(b).
%  Corso: 5069, Docente: ZAFFANELLA Enea
cattedra(5069, 5602, lm, b) :- codice_corso(5069), matricola_docente(5602), laurea(lm), taf(b).
%  Corso: 3027, Docente: ZAFFANELLA Enea
cattedra(3027, 5602, lt, b) :- codice_corso(3027), matricola_docente(5602), laurea(lt), taf(b).
%  Corso: 3027, Docente: ZAFFANELLA Enea
cattedra(3027, 5602, lt, b) :- codice_corso(3027), matricola_docente(5602), laurea(lt), taf(b).

