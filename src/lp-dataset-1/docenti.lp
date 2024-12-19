%  SEZIONE: SSD
ssd(inf).
ssd(mat).
ssd(chim).
ssd(fis).

%  SEZIONE: FASCIE
fascia(td).
fascia(ti).

%  SEZIONE: Docenti
%  ARCERI Vincenzo (33657), SSD caratterizzante: inf/1
matricola_docente(33657).
%  BAGNARA Roberto (5145), SSD caratterizzante: inf/1
matricola_docente(5145).
%  BENINI Anna (26131), SSD caratterizzante: mat/3
matricola_docente(26131).
%  BERGENTI Federico (204741), SSD caratterizzante: inf/1
matricola_docente(204741).
%  BERTINI Flavio (32990), SSD caratterizzante: inf/1
matricola_docente(32990).
%  BONNICI Vincenzo (34181), SSD caratterizzante: inf/1
matricola_docente(34181).
%  BORGHESANI Valentina (12129), SSD caratterizzante: chim/3
matricola_docente(12129).
%  CHIESA Alessandro (11047), SSD caratterizzante: fis/3
matricola_docente(11047).
%  DAL PALU' Alessandro (6625), SSD caratterizzante: inf/1
matricola_docente(6625).
%  DE FILIPPIS Cristiana (34499), SSD caratterizzante: mat/5
matricola_docente(34499).
%  DE PIETRI Roberto (5536), SSD caratterizzante: fis/2
matricola_docente(5536).
%  DI RENZO Francesco (5470), SSD caratterizzante: fis/2
matricola_docente(5470).
%  GUARDASONI Chiara (6801), SSD caratterizzante: mat/8
matricola_docente(6801).
%  IOTTI Eleonora (13027), SSD caratterizzante: inf/1
matricola_docente(13027).
%  MORANDIN Francesco (5804), SSD caratterizzante: mat/6
matricola_docente(5804).
%  MUNARO Andrea (36662), SSD caratterizzante: inf/1
matricola_docente(36662).
%  ZAFFANELLA Enea (5602), SSD caratterizzante: inf/1
matricola_docente(5602).

%  SEZIONE: SSD caratterizzante dei docenti
%  ARCERI Vincenzo (33657), SSD caratterizzante: inf/1
docente(33657, td, inf) :- matricola_docente(33657), fascia(td), ssd(inf).
%  BAGNARA Roberto (5145), SSD caratterizzante: inf/1
docente(5145, ti, inf) :- matricola_docente(5145), fascia(ti), ssd(inf).
%  BENINI Anna (26131), SSD caratterizzante: mat/3
docente(26131, ti, mat) :- matricola_docente(26131), fascia(ti), ssd(mat).
%  BERGENTI Federico (204741), SSD caratterizzante: inf/1
docente(204741, ti, inf) :- matricola_docente(204741), fascia(ti), ssd(inf).
%  BERTINI Flavio (32990), SSD caratterizzante: inf/1
docente(32990, td, inf) :- matricola_docente(32990), fascia(td), ssd(inf).
%  BONNICI Vincenzo (34181), SSD caratterizzante: inf/1
docente(34181, ti, inf) :- matricola_docente(34181), fascia(ti), ssd(inf).
%  BORGHESANI Valentina (12129), SSD caratterizzante: chim/3
docente(12129, td, chim) :- matricola_docente(12129), fascia(td), ssd(chim).
%  CHIESA Alessandro (11047), SSD caratterizzante: fis/3
docente(11047, td, fis) :- matricola_docente(11047), fascia(td), ssd(fis).
%  DAL PALU' Alessandro (6625), SSD caratterizzante: inf/1
docente(6625, ti, inf) :- matricola_docente(6625), fascia(ti), ssd(inf).
%  DE FILIPPIS Cristiana (34499), SSD caratterizzante: mat/5
docente(34499, ti, mat) :- matricola_docente(34499), fascia(ti), ssd(mat).
%  DE PIETRI Roberto (5536), SSD caratterizzante: fis/2
docente(5536, ti, fis) :- matricola_docente(5536), fascia(ti), ssd(fis).
%  DI RENZO Francesco (5470), SSD caratterizzante: fis/2
docente(5470, ti, fis) :- matricola_docente(5470), fascia(ti), ssd(fis).
%  GUARDASONI Chiara (6801), SSD caratterizzante: mat/8
docente(6801, ti, mat) :- matricola_docente(6801), fascia(ti), ssd(mat).
%  IOTTI Eleonora (13027), SSD caratterizzante: inf/1
docente(13027, td, inf) :- matricola_docente(13027), fascia(td), ssd(inf).
%  MORANDIN Francesco (5804), SSD caratterizzante: mat/6
docente(5804, ti, mat) :- matricola_docente(5804), fascia(ti), ssd(mat).
%  MUNARO Andrea (36662), SSD caratterizzante: inf/1
docente(36662, td, inf) :- matricola_docente(36662), fascia(td), ssd(inf).
%  ZAFFANELLA Enea (5602), SSD caratterizzante: inf/1
docente(5602, ti, inf) :- matricola_docente(5602), fascia(ti), ssd(inf).

