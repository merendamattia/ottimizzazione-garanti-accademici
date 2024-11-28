min_garanti(lm, inf, 6).

%  SEZIONE: Tipi di Corso
laurea(lm).

%  SEZIONE: SSD
ssd(inf).

%  SEZIONE: Docenti
%  BAGNARA Roberto (5145), SSD caratterizzante: inf
matricola_docente(5145).
%  BERGENTI Federico (204741), SSD caratterizzante: inf
matricola_docente(204741).
%  BERTINI FLAVIO (32990), SSD caratterizzante: inf
matricola_docente(32990).
%  BONNICI Vincenzo (34181), SSD caratterizzante: inf
matricola_docente(34181).
%  DAL PALU' Alessandro (6625), SSD caratterizzante: inf
matricola_docente(6625).
%  GIUPPONI SELENE (37772), SSD caratterizzante: inf
matricola_docente(37772).
%  GRANATA Donatella (31089), SSD caratterizzante: inf
matricola_docente(31089).
%  IOTTI ELEONORA (13027), SSD caratterizzante: inf
matricola_docente(13027).
%  PESCETTI ANDREA (100162), SSD caratterizzante: inf
matricola_docente(100162).
%  TESI GIOVACCHINO (34246), SSD caratterizzante: inf
matricola_docente(34246).
%  ZAFFANELLA Enea (5602), SSD caratterizzante: inf
matricola_docente(5602).

%  SEZIONE: SSD caratterizzante dei docenti
%  BAGNARA Roberto (5145), SSD caratterizzante: inf
docente_ssd(5145, inf).
%  BERGENTI Federico (204741), SSD caratterizzante: inf
docente_ssd(204741, inf).
%  BERTINI FLAVIO (32990), SSD caratterizzante: inf
docente_ssd(32990, inf).
%  BONNICI Vincenzo (34181), SSD caratterizzante: inf
docente_ssd(34181, inf).
%  DAL PALU' Alessandro (6625), SSD caratterizzante: inf
docente_ssd(6625, inf).
%  GIUPPONI SELENE (37772), SSD caratterizzante: inf
docente_ssd(37772, inf).
%  GRANATA Donatella (31089), SSD caratterizzante: inf
docente_ssd(31089, inf).
%  IOTTI ELEONORA (13027), SSD caratterizzante: inf
docente_ssd(13027, inf).
%  PESCETTI ANDREA (100162), SSD caratterizzante: inf
docente_ssd(100162, inf).
%  TESI GIOVACCHINO (34246), SSD caratterizzante: inf
docente_ssd(34246, inf).
%  ZAFFANELLA Enea (5602), SSD caratterizzante: inf
docente_ssd(5602, inf).

%  SEZIONE: Corsi
%  DEVELOPMENT OF RELIABLE, SAFE AND SECURE SOFTWARE (1009069)
matricola_corso(1009069).
%  LABORATORIO DI INTELLIGENZA ARTIFICIALE (1009073)
matricola_corso(1009073).
%  AGENTI SOFTWARE E SISTEMI MULTI-AGENTE (1009072)
matricola_corso(1009072).
%  BIG DATA E DATA MINING (1009070)
matricola_corso(1009070).
%  ALGORITMI PER L'INTELLIGENZA ARTIFICIALE (1009071)
matricola_corso(1009071).
%  PROGRAMMAZIONE DICHIARATIVA (1009066)
matricola_corso(1009066).
%  SICUREZZA INFORMATICA (1010918)
matricola_corso(1010918).
%  METODI PER ALGORITMI E STRUTTURE DATI (1012414)
matricola_corso(1012414).
%  FONDAMENTI DELL'INTELLIGENZA ARTIFICIALE (1009065)
matricola_corso(1009065).
%  COMUNICAZIONE WEB E DATA JOURNALISM (1008772)
matricola_corso(1008772).
%  Applicazioni industriali dell'intelligenza artificiale (1010245)
matricola_corso(1010245).
%  LINGUAGGI,INTERPRETI E COMPILATORI (1009064)
matricola_corso(1009064).

%  SEZIONE: Relazioni Corsi-Docenti
%  Corso: 1009069, Docente: BAGNARA Roberto
docente_corso(1009069, 5145) :- matricola_corso(1009069), matricola_docente(5145).
%  Corso: 1009073, Docente: BERGENTI Federico
docente_corso(1009073, 204741) :- matricola_corso(1009073), matricola_docente(204741).
%  Corso: 1009072, Docente: BERGENTI Federico
docente_corso(1009072, 204741) :- matricola_corso(1009072), matricola_docente(204741).
%  Corso: 1009070, Docente: BERTINI FLAVIO
docente_corso(1009070, 32990) :- matricola_corso(1009070), matricola_docente(32990).
%  Corso: 1009071, Docente: BONNICI Vincenzo
docente_corso(1009071, 34181) :- matricola_corso(1009071), matricola_docente(34181).
%  Corso: 1009066, Docente: DAL PALU' Alessandro
docente_corso(1009066, 6625) :- matricola_corso(1009066), matricola_docente(6625).
%  Corso: 1010918, Docente: GIUPPONI SELENE
docente_corso(1010918, 37772) :- matricola_corso(1010918), matricola_docente(37772).
%  Corso: 1012414, Docente: GRANATA Donatella
docente_corso(1012414, 31089) :- matricola_corso(1012414), matricola_docente(31089).
%  Corso: 1009065, Docente: IOTTI ELEONORA
docente_corso(1009065, 13027) :- matricola_corso(1009065), matricola_docente(13027).
%  Corso: 1008772, Docente: PESCETTI ANDREA
docente_corso(1008772, 100162) :- matricola_corso(1008772), matricola_docente(100162).
%  Corso: 1010245, Docente: TESI GIOVACCHINO
docente_corso(1010245, 34246) :- matricola_corso(1010245), matricola_docente(34246).
%  Corso: 1009064, Docente: ZAFFANELLA Enea
docente_corso(1009064, 5602) :- matricola_corso(1009064), matricola_docente(5602).

%  SEZIONE: Informazioni Corsi
%  Corso: 1009069 (lm), Docente: BAGNARA Roberto
corso(1009069, lm, inf) :- matricola_corso(1009069), laurea(lm), ssd(inf).
%  Corso: 1009073 (lm), Docente: BERGENTI Federico
corso(1009073, lm, inf) :- matricola_corso(1009073), laurea(lm), ssd(inf).
%  Corso: 1009072 (lm), Docente: BERGENTI Federico
corso(1009072, lm, inf) :- matricola_corso(1009072), laurea(lm), ssd(inf).
%  Corso: 1009070 (lm), Docente: BERTINI FLAVIO
corso(1009070, lm, inf) :- matricola_corso(1009070), laurea(lm), ssd(inf).
%  Corso: 1009071 (lm), Docente: BONNICI Vincenzo
corso(1009071, lm, inf) :- matricola_corso(1009071), laurea(lm), ssd(inf).
%  Corso: 1009066 (lm), Docente: DAL PALU' Alessandro
corso(1009066, lm, inf) :- matricola_corso(1009066), laurea(lm), ssd(inf).
%  Corso: 1010918 (lm), Docente: GIUPPONI SELENE
corso(1010918, lm, inf) :- matricola_corso(1010918), laurea(lm), ssd(inf).
%  Corso: 1012414 (lm), Docente: GRANATA Donatella
corso(1012414, lm, inf) :- matricola_corso(1012414), laurea(lm), ssd(inf).
%  Corso: 1009065 (lm), Docente: IOTTI ELEONORA
corso(1009065, lm, inf) :- matricola_corso(1009065), laurea(lm), ssd(inf).
%  Corso: 1008772 (lm), Docente: PESCETTI ANDREA
corso(1008772, lm, inf) :- matricola_corso(1008772), laurea(lm), ssd(inf).
%  Corso: 1010245 (lm), Docente: TESI GIOVACCHINO
corso(1010245, lm, inf) :- matricola_corso(1010245), laurea(lm), ssd(inf).
%  Corso: 1009064 (lm), Docente: ZAFFANELLA Enea
corso(1009064, lm, inf) :- matricola_corso(1009064), laurea(lm), ssd(inf).
