%  SEZIONE: Tipi di Corso
laurea(lt).
laurea(lm).

%  SEZIONE: SSD
ssd(fis).
ssd(mat).
ssd(inf).
ssd(chim).
ssd(icar).

%  SEZIONE: TAF
taf(c).
taf(b).
taf(a).
taf(d).
taf(f).

%  SEZIONE: Corsi
%  FISICA (3026)
codice_corso(3026).
%  FISICA (5036)
codice_corso(5036).
%  MATEMATICA (3030)
codice_corso(3030).
%  MATEMATICA (5037)
codice_corso(5037).
%  INFORMATICA (3027)
codice_corso(3027).
%  SCIENZE INFORMATICHE (5069)
codice_corso(5069).

%  SEZIONE: Informazioni Corsi
%  Corso: 3026 (lt)
corso(3026, lt, chim) :- codice_corso(3026), laurea(lt), ssd(chim).
%  Corso: 3026 (lt)
corso(3026, lt, fis) :- codice_corso(3026), laurea(lt), ssd(fis).
%  Corso: 3026 (lt)
corso(3026, lt, mat) :- codice_corso(3026), laurea(lt), ssd(mat).
%  Corso: 5036 (lm)
corso(5036, lm, fis) :- codice_corso(5036), laurea(lm), ssd(fis).
%  Corso: 3030 (lt)
corso(3030, lt, inf) :- codice_corso(3030), laurea(lt), ssd(inf).
%  Corso: 3030 (lt)
corso(3030, lt, mat) :- codice_corso(3030), laurea(lt), ssd(mat).
%  Corso: 5037 (lm)
corso(5037, lm, mat) :- codice_corso(5037), laurea(lm), ssd(mat).
%  Corso: 3027 (lt)
corso(3027, lt, inf) :- codice_corso(3027), laurea(lt), ssd(inf).
%  Corso: 3027 (lt)
corso(3027, lt, fis) :- codice_corso(3027), laurea(lt), ssd(fis).
%  Corso: 3027 (lt)
corso(3027, lt, mat) :- codice_corso(3027), laurea(lt), ssd(mat).
%  Corso: 5069 (lm)
corso(5069, lm, inf) :- codice_corso(5069), laurea(lm), ssd(inf).

%  SEZIONE: Relazioni Corsi-Docenti
%  Corso: 3026, Docente: ABBRUZZETTI Stefania
cattedra(3026, 6527, lt, c) :- codice_corso(3026), matricola_docente(6527), laurea(lt), taf(c).
%  Corso: 5036, Docente: ABBRUZZETTI Stefania
cattedra(5036, 6527, lm, b) :- codice_corso(5036), matricola_docente(6527), laurea(lm), taf(b).
%  Corso: 3026, Docente: ACERBI Emilio Daniele Giovanni
cattedra(3026, 4397, lt, a) :- codice_corso(3026), matricola_docente(4397), laurea(lt), taf(a).
%  Corso: 3030, Docente: AIMI Alessandra
cattedra(3030, 4642, lt, b) :- codice_corso(3030), matricola_docente(4642), laurea(lt), taf(b).
%  Corso: 5037, Docente: AIMI Alessandra
cattedra(5037, 4642, lm, b) :- codice_corso(5037), matricola_docente(4642), laurea(lm), taf(b).
%  Corso: 3026, Docente: ALLODI Giuseppe
cattedra(3026, 6627, lt, b) :- codice_corso(3026), matricola_docente(6627), laurea(lt), taf(b).
%  Corso: 5036, Docente: ALLODI Giuseppe
cattedra(5036, 6627, lm, b) :- codice_corso(5036), matricola_docente(6627), laurea(lm), taf(b).
%  Corso: 3030, Docente: APPEL Andrea
cattedra(3030, 29217, lt, a) :- codice_corso(3030), matricola_docente(29217), laurea(lt), taf(a).
%  Corso: 5037, Docente: APPEL Andrea
cattedra(5037, 29217, lm, b) :- codice_corso(5037), matricola_docente(29217), laurea(lm), taf(b).
%  Corso: 3030, Docente: APPEL Andrea
cattedra(3030, 29217, lt, d) :- codice_corso(3030), matricola_docente(29217), laurea(lt), taf(d).
%  Corso: 3027, Docente: ARCERI Vincenzo
cattedra(3027, 33657, lt, b) :- codice_corso(3027), matricola_docente(33657), laurea(lt), taf(b).
%  Corso: 3027, Docente: ARCERI Vincenzo
cattedra(3027, 33657, lt, a) :- codice_corso(3027), matricola_docente(33657), laurea(lt), taf(a).
%  Corso: 3027, Docente: BAGNARA Roberto
cattedra(3027, 5145, lt, b) :- codice_corso(3027), matricola_docente(5145), laurea(lt), taf(b).
%  Corso: 5069, Docente: BAGNARA Roberto
cattedra(5069, 5145, lm, b) :- codice_corso(5069), matricola_docente(5145), laurea(lm), taf(b).
%  Corso: 3026, Docente: BARALDI Andrea
cattedra(3026, 5428, lt, b) :- codice_corso(3026), matricola_docente(5428), laurea(lt), taf(b).
%  Corso: 3030, Docente: BARONI Paolo
cattedra(3030, 15874, lt, a) :- codice_corso(3030), matricola_docente(15874), laurea(lt), taf(a).
%  Corso: 5037, Docente: BELLONI Marino
cattedra(5037, 4768, lm, b) :- codice_corso(5037), matricola_docente(4768), laurea(lm), taf(b).
%  Corso: 3030, Docente: BELLONI Marino
cattedra(3030, 4768, lt, c) :- codice_corso(3030), matricola_docente(4768), laurea(lt), taf(c).
%  Corso: 3027, Docente: BENINI Anna
cattedra(3027, 26131, lt, a) :- codice_corso(3027), matricola_docente(26131), laurea(lt), taf(a).
%  Corso: 3027, Docente: BERGENTI Federico
cattedra(3027, 204741, lt, b) :- codice_corso(3027), matricola_docente(204741), laurea(lt), taf(b).
%  Corso: 5069, Docente: BERGENTI Federico
cattedra(5069, 204741, lm, b) :- codice_corso(5069), matricola_docente(204741), laurea(lm), taf(b).
%  Corso: 5069, Docente: BERGENTI Federico
cattedra(5069, 204741, lm, b) :- codice_corso(5069), matricola_docente(204741), laurea(lm), taf(b).
%  Corso: 5036, Docente: BERSANI Danilo
cattedra(5036, 5046, lm, c) :- codice_corso(5036), matricola_docente(5046), laurea(lm), taf(c).
%  Corso: 3026, Docente: BERSANI Danilo
cattedra(3026, 5046, lt, b) :- codice_corso(3026), matricola_docente(5046), laurea(lt), taf(b).
%  Corso: 3027, Docente: BERTINI FLAVIO
cattedra(3027, 32990, lt, b) :- codice_corso(3027), matricola_docente(32990), laurea(lt), taf(b).
%  Corso: 5069, Docente: BERTINI FLAVIO
cattedra(5069, 32990, lm, b) :- codice_corso(5069), matricola_docente(32990), laurea(lm), taf(b).
%  Corso: 3026, Docente: BILIOTTI Leonardo
cattedra(3026, 7136, lt, a) :- codice_corso(3026), matricola_docente(7136), laurea(lt), taf(a).
%  Corso: 5037, Docente: BILIOTTI Leonardo
cattedra(5037, 7136, lm, c) :- codice_corso(5037), matricola_docente(7136), laurea(lm), taf(c).
%  Corso: 5037, Docente: BISI Marzia
cattedra(5037, 6563, lm, b) :- codice_corso(5037), matricola_docente(6563), laurea(lm), taf(b).
%  Corso: 5037, Docente: BISI Marzia
cattedra(5037, 6563, lm, d) :- codice_corso(5037), matricola_docente(6563), laurea(lm), taf(d).
%  Corso: 3030, Docente: BONINI Marisa
cattedra(3030, 4490, lt, c) :- codice_corso(3030), matricola_docente(4490), laurea(lt), taf(c).
%  Corso: 3026, Docente: BONINI Marisa
cattedra(3026, 4490, lt, b) :- codice_corso(3026), matricola_docente(4490), laurea(lt), taf(b).
%  Corso: 3027, Docente: BONNICI Vincenzo
cattedra(3027, 34181, lt, b) :- codice_corso(3027), matricola_docente(34181), laurea(lt), taf(b).
%  Corso: 5069, Docente: BONNICI Vincenzo
cattedra(5069, 34181, lm, b) :- codice_corso(5069), matricola_docente(34181), laurea(lm), taf(b).
%  Corso: 3027, Docente: BONNICI Vincenzo
cattedra(3027, 34181, lt, b) :- codice_corso(3027), matricola_docente(34181), laurea(lt), taf(b).
%  Corso: 3027, Docente: BORGHESANI VALENTINA
cattedra(3027, 12129, lt, c) :- codice_corso(3027), matricola_docente(12129), laurea(lt), taf(c).
%  Corso: 3026, Docente: BOSIO Alessio
cattedra(3026, 4271, lt, c) :- codice_corso(3026), matricola_docente(4271), laurea(lt), taf(c).
%  Corso: 5036, Docente: BURIONI Raffaella
cattedra(5036, 5555, lm, b) :- codice_corso(5036), matricola_docente(5555), laurea(lm), taf(b).
%  Corso: 3026, Docente: BURIONI Raffaella
cattedra(3026, 5555, lt, c) :- codice_corso(3026), matricola_docente(5555), laurea(lt), taf(c).
%  Corso: 3030, Docente: Cagnetti Filippo
cattedra(3030, 41973, lt, b) :- codice_corso(3030), matricola_docente(41973), laurea(lt), taf(b).
%  Corso: 5036, Docente: CARRETTA Stefano
cattedra(5036, 206887, lm, b) :- codice_corso(5036), matricola_docente(206887), laurea(lm), taf(b).
%  Corso: 3026, Docente: CARRETTA Stefano
cattedra(3026, 206887, lt, a) :- codice_corso(3026), matricola_docente(206887), laurea(lt), taf(a).
%  Corso: 5036, Docente: CASSI Davide
cattedra(5036, 4875, lm, b) :- codice_corso(5036), matricola_docente(4875), laurea(lm), taf(b).
%  Corso: 3030, Docente: CATTANEO Andrea
cattedra(3030, 13727, lt, b) :- codice_corso(3030), matricola_docente(13727), laurea(lt), taf(b).
%  Corso: 3030, Docente: CATTANEO Andrea
cattedra(3030, 13727, lt, b) :- codice_corso(3030), matricola_docente(13727), laurea(lt), taf(b).
%  Corso: 3030, Docente: CELADA Pietro
cattedra(3030, 5426, lt, b) :- codice_corso(3030), matricola_docente(5426), laurea(lt), taf(b).
%  Corso: 5069, Docente: CHIESA Alessandro
cattedra(5069, 11047, lm, c) :- codice_corso(5069), matricola_docente(11047), laurea(lm), taf(c).
%  Corso: 5036, Docente: CRISTOFOLINI Luigi
cattedra(5036, 5163, lm, b) :- codice_corso(5036), matricola_docente(5163), laurea(lm), taf(b).
%  Corso: 3026, Docente: CRISTOFOLINI Luigi
cattedra(3026, 5163, lt, b) :- codice_corso(3026), matricola_docente(5163), laurea(lt), taf(b).
%  Corso: 3026, Docente: CUGINI Francesco
cattedra(3026, 11488, lt, f) :- codice_corso(3026), matricola_docente(11488), laurea(lt), taf(f).
%  Corso: 3026, Docente: CUGINI Francesco
cattedra(3026, 11488, lt, b) :- codice_corso(3026), matricola_docente(11488), laurea(lt), taf(b).
%  Corso: 5036, Docente: CUGINI Francesco
cattedra(5036, 11488, lm, b) :- codice_corso(5036), matricola_docente(11488), laurea(lm), taf(b).
%  Corso: 3027, Docente: DAL PALU' Alessandro
cattedra(3027, 6625, lt, a) :- codice_corso(3027), matricola_docente(6625), laurea(lt), taf(a).
%  Corso: 5069, Docente: DAL PALU' Alessandro
cattedra(5069, 6625, lm, b) :- codice_corso(5069), matricola_docente(6625), laurea(lm), taf(b).
%  Corso: 3027, Docente: DAL PALU' Alessandro
cattedra(3027, 6625, lt, b) :- codice_corso(3027), matricola_docente(6625), laurea(lt), taf(b).
%  Corso: 3026, Docente: D'AMICO Guido
cattedra(3026, 26134, lt, b) :- codice_corso(3026), matricola_docente(26134), laurea(lt), taf(b).
%  Corso: 3027, Docente: DE FILIPPIS Cristiana
cattedra(3027, 34499, lt, a) :- codice_corso(3027), matricola_docente(34499), laurea(lt), taf(a).
%  Corso: 3027, Docente: DE PIETRI Roberto
cattedra(3027, 5536, lt, a) :- codice_corso(3027), matricola_docente(5536), laurea(lt), taf(a).
%  Corso: 5036, Docente: DE PIETRI Roberto
cattedra(5036, 5536, lm, c) :- codice_corso(5036), matricola_docente(5536), laurea(lm), taf(c).
%  Corso: 3026, Docente: DE RENZI Roberto
cattedra(3026, 3708, lt, b) :- codice_corso(3026), matricola_docente(3708), laurea(lt), taf(b).
%  Corso: 5037, Docente: DI BARI Maria
cattedra(5037, 5920, lm, c) :- codice_corso(5037), matricola_docente(5920), laurea(lm), taf(c).
%  Corso: 3026, Docente: DI RENZO Francesco
cattedra(3026, 5470, lt, c) :- codice_corso(3026), matricola_docente(5470), laurea(lt), taf(c).
%  Corso: 3026, Docente: DI RENZO Francesco
cattedra(3026, 5470, lt, b) :- codice_corso(3026), matricola_docente(5470), laurea(lt), taf(b).
%  Corso: 5069, Docente: DI RENZO Francesco
cattedra(5069, 5470, lm, c) :- codice_corso(5069), matricola_docente(5470), laurea(lm), taf(c).
%  Corso: 5036, Docente: FORNARI Roberto
cattedra(5036, 11154, lm, c) :- codice_corso(5036), matricola_docente(11154), laurea(lm), taf(c).
%  Corso: 3026, Docente: GHIDINI Massimo
cattedra(3026, 5463, lt, b) :- codice_corso(3026), matricola_docente(5463), laurea(lt), taf(b).
%  Corso: 5036, Docente: GRIGUOLO Luca
cattedra(5036, 5441, lm, c) :- codice_corso(5036), matricola_docente(5441), laurea(lm), taf(c).
%  Corso: 5036, Docente: GRIGUOLO Luca
cattedra(5036, 5441, lm, c) :- codice_corso(5036), matricola_docente(5441), laurea(lm), taf(c).
%  Corso: 3026, Docente: GRIGUOLO Luca
cattedra(3026, 5441, lt, c) :- codice_corso(3026), matricola_docente(5441), laurea(lt), taf(c).
%  Corso: 3030, Docente: GROPPI Maria
cattedra(3030, 4912, lt, b) :- codice_corso(3030), matricola_docente(4912), laurea(lt), taf(b).
%  Corso: 3030, Docente: GROPPI Maria
cattedra(3030, 4912, lt, d) :- codice_corso(3030), matricola_docente(4912), laurea(lt), taf(d).
%  Corso: 5037, Docente: GUARDASONI Chiara
cattedra(5037, 6801, lm, d) :- codice_corso(5037), matricola_docente(6801), laurea(lm), taf(d).
%  Corso: 5037, Docente: GUARDASONI Chiara
cattedra(5037, 6801, lm, c) :- codice_corso(5037), matricola_docente(6801), laurea(lm), taf(c).
%  Corso: 3027, Docente: GUARDASONI Chiara
cattedra(3027, 6801, lt, c) :- codice_corso(3027), matricola_docente(6801), laurea(lt), taf(c).
%  Corso: 5069, Docente: IOTTI ELEONORA
cattedra(5069, 13027, lm, b) :- codice_corso(5069), matricola_docente(13027), laurea(lm), taf(b).
%  Corso: 3027, Docente: IOTTI ELEONORA
cattedra(3027, 13027, lt, a) :- codice_corso(3027), matricola_docente(13027), laurea(lt), taf(a).
%  Corso: 3030, Docente: LORENZI Luca Francesco Giuseppe
cattedra(3030, 5599, lt, a) :- codice_corso(3030), matricola_docente(5599), laurea(lt), taf(a).
%  Corso: 5036, Docente: LOSI Aba
cattedra(5036, 6121, lm, c) :- codice_corso(5036), matricola_docente(6121), laurea(lm), taf(c).
%  Corso: 3030, Docente: MEDORI Costantino
cattedra(3030, 5104, lt, a) :- codice_corso(3030), matricola_docente(5104), laurea(lt), taf(a).
%  Corso: 5037, Docente: MEDORI Costantino
cattedra(5037, 5104, lm, b) :- codice_corso(5037), matricola_docente(5104), laurea(lm), taf(b).
%  Corso: 5036, Docente: MENEGHELLI Carlo
cattedra(5036, 33665, lm, b) :- codice_corso(5036), matricola_docente(33665), laurea(lm), taf(b).
%  Corso: 3026, Docente: MENEGHELLI Carlo
cattedra(3026, 33665, lt, c) :- codice_corso(3026), matricola_docente(33665), laurea(lt), taf(c).
%  Corso: 5069, Docente: MORANDIN Francesco
cattedra(5069, 5804, lm, c) :- codice_corso(5069), matricola_docente(5804), laurea(lm), taf(c).
%  Corso: 3030, Docente: MORANDIN Francesco
cattedra(3030, 5804, lt, b) :- codice_corso(3030), matricola_docente(5804), laurea(lt), taf(b).
%  Corso: 3030, Docente: MORINI Fiorenza
cattedra(3030, 8733, lt, b) :- codice_corso(3030), matricola_docente(8733), laurea(lt), taf(b).
%  Corso: 5037, Docente: MORINI Massimiliano
cattedra(5037, 10285, lm, b) :- codice_corso(5037), matricola_docente(10285), laurea(lm), taf(b).
%  Corso: 3027, Docente: MUNARO Andrea
cattedra(3027, 36662, lt, b) :- codice_corso(3027), matricola_docente(36662), laurea(lt), taf(b).
%  Corso: 3030, Docente: MUNARO Andrea
cattedra(3030, 36662, lt, a) :- codice_corso(3030), matricola_docente(36662), laurea(lt), taf(a).
%  Corso: 3026, Docente: ONUORAH IFEANYI JOHN
cattedra(3026, 17206, lt, b) :- codice_corso(3026), matricola_docente(17206), laurea(lt), taf(b).
%  Corso: 3026, Docente: ORSI Davide
cattedra(3026, 8854, lt, b) :- codice_corso(3026), matricola_docente(8854), laurea(lt), taf(b).
%  Corso: 3030, Docente: PANIZZI Stefano
cattedra(3030, 4499, lt, a) :- codice_corso(3030), matricola_docente(4499), laurea(lt), taf(a).
%  Corso: 5036, Docente: PARISINI Antonella
cattedra(5036, 4336, lm, c) :- codice_corso(5036), matricola_docente(4336), laurea(lm), taf(c).
%  Corso: 3026, Docente: PARISINI Antonella
cattedra(3026, 4336, lt, b) :- codice_corso(3026), matricola_docente(4336), laurea(lt), taf(b).
%  Corso: 3030, Docente: PASQUERO Stefano
cattedra(3030, 4625, lt, b) :- codice_corso(3030), matricola_docente(4625), laurea(lt), taf(b).
%  Corso: 3026, Docente: PAVESI Maura
cattedra(3026, 6653, lt, c) :- codice_corso(3026), matricola_docente(6653), laurea(lt), taf(c).
%  Corso: 3026, Docente: PIETRONI MASSIMO
cattedra(3026, 100649, lt, b) :- codice_corso(3026), matricola_docente(100649), laurea(lt), taf(b).
%  Corso: 5036, Docente: PIETRONI MASSIMO
cattedra(5036, 100649, lm, b) :- codice_corso(5036), matricola_docente(100649), laurea(lm), taf(b).
%  Corso: 5036, Docente: POLVERINI Eugenia
cattedra(5036, 6086, lm, b) :- codice_corso(5036), matricola_docente(6086), laurea(lm), taf(b).
%  Corso: 5036, Docente: PONTIROLI Daniele
cattedra(5036, 253752, lm, b) :- codice_corso(5036), matricola_docente(253752), laurea(lm), taf(b).
%  Corso: 5036, Docente: RICCO' Mauro
cattedra(5036, 4370, lm, c) :- codice_corso(5036), matricola_docente(4370), laurea(lm), taf(c).
%  Corso: 3026, Docente: ROGOLINO Dominga
cattedra(3026, 6119, lt, a) :- codice_corso(3026), matricola_docente(6119), laurea(lt), taf(a).
%  Corso: 5037, Docente: ROYER CARFAGNI Gianni
cattedra(5037, 5088, lm, d) :- codice_corso(5037), matricola_docente(5088), laurea(lm), taf(d).
%  Corso: 5036, Docente: SANTINI Paolo
cattedra(5036, 6762, lm, f) :- codice_corso(5036), matricola_docente(6762), laurea(lm), taf(f).
%  Corso: 5036, Docente: SANTINI Paolo
cattedra(5036, 6762, lm, b) :- codice_corso(5036), matricola_docente(6762), laurea(lm), taf(b).
%  Corso: 3026, Docente: SOLZI Massimo
cattedra(3026, 4373, lt, c) :- codice_corso(3026), matricola_docente(4373), laurea(lt), taf(c).
%  Corso: 3026, Docente: SOLZI Massimo
cattedra(3026, 4373, lt, a) :- codice_corso(3026), matricola_docente(4373), laurea(lt), taf(a).
%  Corso: 5037, Docente: TOMASSINI Adriano
cattedra(5037, 5252, lm, b) :- codice_corso(5037), matricola_docente(5252), laurea(lm), taf(b).
%  Corso: 3030, Docente: TOMASSINI Adriano
cattedra(3030, 5252, lt, a) :- codice_corso(3030), matricola_docente(5252), laurea(lt), taf(a).
%  Corso: 3030, Docente: TOMASSINI Adriano
cattedra(3030, 5252, lt, b) :- codice_corso(3030), matricola_docente(5252), laurea(lt), taf(b).
%  Corso: 5036, Docente: VIAPPIANI Cristiano
cattedra(5036, 4696, lm, b) :- codice_corso(5036), matricola_docente(4696), laurea(lm), taf(b).
%  Corso: 5036, Docente: WIMBERGER Sandro Marcel
cattedra(5036, 11350, lm, b) :- codice_corso(5036), matricola_docente(11350), laurea(lm), taf(b).
%  Corso: 3030, Docente: ZACCAGNINI Alessandro
cattedra(3030, 4609, lt, d) :- codice_corso(3030), matricola_docente(4609), laurea(lt), taf(d).
%  Corso: 3030, Docente: ZACCAGNINI Alessandro
cattedra(3030, 4609, lt, b) :- codice_corso(3030), matricola_docente(4609), laurea(lt), taf(b).
%  Corso: 5037, Docente: ZACCAGNINI Alessandro
cattedra(5037, 4609, lm, c) :- codice_corso(5037), matricola_docente(4609), laurea(lm), taf(c).
%  Corso: 5069, Docente: ZAFFANELLA Enea
cattedra(5069, 5602, lm, b) :- codice_corso(5069), matricola_docente(5602), laurea(lm), taf(b).
%  Corso: 3027, Docente: ZAFFANELLA Enea
cattedra(3027, 5602, lt, b) :- codice_corso(3027), matricola_docente(5602), laurea(lt), taf(b).
%  Corso: 3027, Docente: ZAFFANELLA Enea
cattedra(3027, 5602, lt, b) :- codice_corso(3027), matricola_docente(5602), laurea(lt), taf(b).
%  Corso: 5037, Docente: ZEDDA MICHELA
cattedra(5037, 15248, lm, c) :- codice_corso(5037), matricola_docente(15248), laurea(lm), taf(c).
%  Corso: 3030, Docente: ZEDDA MICHELA
cattedra(3030, 15248, lt, a) :- codice_corso(3030), matricola_docente(15248), laurea(lt), taf(a).

