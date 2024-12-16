import os
import pandas as pd
import math

class DatasetManager:
    """
    Classe per la gestione di file di dataset e la generazione di file ASP strutturati.

    La classe permette di:
    - Recuperare informazioni sui corsi e sui professori da file dataset.
    - Generare file ASP (.lp) contenenti i dati processati e strutturati.
    """

    def __init__(self, dataset_path="dataset/"):
        """
        Inizializza la classe DatasetManager con il percorso della cartella contenente i file di dataset.

        :param dataset_path: Percorso alla cartella contenente i file di dataset. Default: "dataset/".
        :type dataset_path: str
        """
        self.dataset_path = dataset_path

    def get_courses(self):
        """
        Ottiene un dizionario dei corsi basandosi sui file presenti nella cartella del dataset.

        :return: Dizionario con chiavi come "Cod. Corso di Studio" e valori come "Overview".
        :rtype: dict
        :raises FileNotFoundError: Se la cartella del dataset non esiste.
        """
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Errore: il file '{self.dataset_path}' non esiste.")
        
        df = pd.read_csv(self.dataset_path, dtype=str, sep=',')
        # print(df)
        return df.set_index("Cod. Corso di Studio")["Overview"].to_dict()
    
    def get_professors(self):
        """
        Ottiene un dizionario che associa ciascun corso ai professori tramite la loro matricola.

        :return: Dizionario con chiavi come "Cod. Corso di Studio" e valori come insiemi di matricole.
        :rtype: dict
        :raises FileNotFoundError: Se la cartella del dataset non esiste.
        """
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Errore: il file '{self.dataset_path}' non esiste.")
        
        with open(self.dataset_path) as f:
            # Skip prima riga
            f.readline()
            profs = dict()
            for line in f.readlines():
                code, mat = line.strip().split(",")
                if not code in profs:
                    profs[code] = set()
                
                profs[code].add(mat)
            return profs

    def scrivi_ministeriali(self, df, filename):
        """
        Genera un file ASP contenente i parametri ministeriali per i corsi.

        :param df: DataFrame contenente i dati relativi ai corsi.
        :type df: pandas.DataFrame
        :param filename: Nome del file di output (senza estensione).
        :type filename: str
        :raises Exception: Se si verifica un errore durante la scrittura del file.
        """
        
        output_dir = 'lp'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        comment_character = '% '
        filepath = os.path.join(output_dir, filename + '.lp')
        
        parametri_ministeriali_minimi = {
            "lt": (9, 5, 4, 2),
            "lm": (6, 4, 2, 1),
            "lm5": (15, 8, 7, 3),
            "lm6": (18, 10, 8, 4),
            "lcpa": (5, 3, 2, 1),
            "lcpb": (4, 2, 2, 1),
            "lcpc": (3, 1, 2, 1)
        }

        try:
            with open(filepath, "w") as file:
                file.write(f"{comment_character} SEZIONE: Garanti minimi per corso (codice_corso, minimo_complessivo, docenti_ti, docenti_td, max_docenti_contratto)\n")

                # print(df)
                
                for _, row in df.iterrows():
                    tipo_corso = row["Cod. Tipo Corso"].lower()
                    codice_corso = row["Cod. Corso di Studio"]
                    
                    if tipo_corso in parametri_ministeriali_minimi:
                        minimo_complessivo, minimo_ti, massimo_td, massimo_contratti = parametri_ministeriali_minimi[tipo_corso]
                    else:
                        raise ValueError(f"Cod. Tipo Corso ({tipo_corso}) non coerente per il corso {codice_corso}")
                    
                    if pd.isna(row['Immatricolati']):
                        pass
                    else:
                        immatricolati = int(row["Immatricolati"])

                        massimo_teorico = int(row["Massimo Teorico"])
                        # il calcolo della W si applica solo se si superano i massimi teorici
                        if immatricolati > massimo_teorico:
                            w = (immatricolati / (1.0 * massimo_teorico)) - 1
                            if w < 0:
                                raise ValueError("w < 0")
                            
                            minimo_complessivo = math.floor(minimo_complessivo * (1 + w))
                            # variano solo i docenti a tempo indeterminato
                            minimo_ti = math.floor(minimo_ti * (1 + w))
                            
                            # il massimo dei contratti non viene aumentato
                            # massimo_contratti = math.floor(massimo_contratti * (1 + w))

                    file.write(f"ministeriale({codice_corso}, {minimo_complessivo}, {minimo_ti}, {massimo_td}, {massimo_contratti}).\n")
            
            print(f"Dati salvati con successo in: {filepath}")
        except Exception as e:
            raise Exception(f"Errore durante il salvataggio dei dati su '{filepath}': {e}")
    
    def scrivi_presidenti(self, df, filename):
        output_dir = 'lp'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        comment_character = '% '
        # filepath = os.path.join(self.dataset_path, filename + '.lp')
        filepath = os.path.join(output_dir, filename + '.lp')
        # todo: continuare qui
        
        
    def scrivi_coperture(self, df, filename):
        """
        Genera un file ASP contenente informazioni sui corsi, TAF e SSD.

        :param df: DataFrame contenente i dati relativi ai corsi.
        :type df: pandas.DataFrame
        :param filename: Nome del file di output (senza estensione).
        :type filename: str
        :raises Exception: Se si verifica un errore durante la scrittura del file.
        """
        # Crea la cartella 'lp' se non esiste
        output_dir = 'lp'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        comment_character = '% '
        # filepath = os.path.join(self.dataset_path, filename + '.lp')
        filepath = os.path.join(output_dir, filename + '.lp')

        # Set per tracciare valori già scritti
        docenti_aggiunti = set()
        corsi_aggiunti = set()
        tipi_corso_aggiunti = set()
        ssd_aggiunti = set()
        taf_aggiunti = set()

        # Rimuove eventuali NaN e converte i valori in numeri interi
        df['Cod. Corso di Studio'] = df['Cod. Corso di Studio'].fillna(0).astype(int)

        accepted_tafs = set(["a", "b"])
        
        # Dict per memorizzare gli ssd di un corso di laurea (il codice è l'identificativo)
        corso_ssds = dict()
        for _, row in df.iterrows():
            
            if not (row["TAF"].lower() in accepted_tafs):
                continue
            
            if not (row["Cod. Corso di Studio"] in corso_ssds):
                corso_ssds[row["Cod. Corso di Studio"]] = set()
            
            ssd = row["SSD"].split("/")
            if len(ssd) < 2:
                # print(f"Errore: {row['Cod. Corso di Studio']} non ha un SSD valido")
                raise Exception(f"Errore: {row['Cod. Corso di Studio']} non ha un SSD valido")
                # continue
            
            
            ssd[0] = ssd[0].strip().replace("-", "")
            corso_ssds[row["Cod. Corso di Studio"]].add(ssd[0])
        
        try:
            with open(filepath, 'w') as file:
                
                # Scrive la sezione dei tipi di corso
                file.write(f"{comment_character} SEZIONE: Tipi di Corso\n")
                for _, row in df.iterrows():
                    # Non posso usare le lettere in maiuscolo perchè possono essere scambiate per variabili e non atomi
                    tipo_corso = row['Cod. Tipo Corso'].lower()

                    if tipo_corso not in tipi_corso_aggiunti:
                        file.write(f"laurea({tipo_corso}).\n")
                        tipi_corso_aggiunti.add(tipo_corso)
                file.write("\n")

                # Scrive la sezione dei vari SSD
                file.write(f"{comment_character} SEZIONE: SSD\n")
                for _, row in df.iterrows():
                    
                    ssd = row['SSD'].split('/')
                    if len(ssd) < 2:
                        continue
                    
                    settore = ssd[0].lower()
                    settore = settore.replace('-', '')

                    if settore not in ssd_aggiunti:
                        file.write(f"ssd({settore}).\n")
                        ssd_aggiunti.add(settore)
                file.write("\n")

                # Scrive la sezione dei TAF
                file.write(f"{comment_character} SEZIONE: TAF\n")
                for _, row in df.iterrows():
                    taf = row['TAF'].lower()

                    if taf not in taf_aggiunti:
                        # file.write(f"{comment_character} {nome_corso} ({codice_corso})\n")
                        file.write(f"taf({taf}).\n")
                        taf_aggiunti.add(taf)
                file.write("\n")

                # Scrive la sezione dei corsi
                file.write(f"{comment_character} SEZIONE: Corsi\n")
                for _, row in df.iterrows():
                    codice_corso = int(float(row['Cod. Corso di Studio']))
                    nome_corso = row['Des. Corso di Studio']

                    if codice_corso not in corsi_aggiunti:
                        file.write(f"{comment_character} {nome_corso} ({codice_corso})\n")
                        file.write(f"codice_corso({codice_corso}).\n")
                        corsi_aggiunti.add(codice_corso)
                file.write("\n")

                corsi_aggiunti = set()
                
                # Scrive le informazioni complete sui corsi
                file.write(f"{comment_character} SEZIONE: Informazioni Corsi\n")
                for _, row in df.iterrows():
                    codice_corso = int(float(row['Cod. Corso di Studio']))
                    tipo_corso = row['Cod. Tipo Corso'].lower()
                    
                    if codice_corso not in corsi_aggiunti:
                        # print("Codice corso:", codice_corso)
                        if not codice_corso in corso_ssds:
                            print(f"Errore: il corso {codice_corso} non ha SSD validi")
                            continue
                        
                        settori = corso_ssds[codice_corso]
                        for ssd in settori:
                            settore = ssd.lower()
                            file.write(f"{comment_character} Corso: {codice_corso} ({tipo_corso})\n")
                            file.write(f"corso({codice_corso}, {tipo_corso}, {settore}) :- codice_corso({codice_corso}), laurea({tipo_corso}), ssd({settore}).\n")
                            corsi_aggiunti.add(codice_corso)

                file.write("\n")
                
                
                # Scrive le relazioni tra corsi e docenti
                file.write(f"{comment_character} SEZIONE: Relazioni Corsi-Docenti\n")
                for _, row in df.iterrows():
                    if not row['Matricola'] or row['Matricola'] is None or row['Matricola'].lower() == 'nan':
                        continue
                    else:
                        matricola_docente = int(float(row['Matricola']))

                    codice_corso = int(float(row['Cod. Corso di Studio']))
                    nome_docente = row['Cognome'] + " " + row['Nome']
                    tipo_corso = row['Cod. Tipo Corso'].lower()
                    taf = row['TAF'].lower()

                    file.write(f"{comment_character} Corso: {codice_corso}, Docente: {nome_docente}\n")
                    file.write(f"cattedra({codice_corso}, {matricola_docente}, {tipo_corso}, {taf}) :- codice_corso({codice_corso}), matricola_docente({matricola_docente}), laurea({tipo_corso}), taf({taf}).\n")
                file.write("\n")

            print(f"Dati salvati con successo in: {filepath}")
        except Exception as e:
            raise Exception(f"Errore durante il salvataggio dei dati su '{filepath}': {e}")
    
    def scrivi_docenti(self, df, filename):
        """
        Genera un file ASP contenente informazioni sui docenti.

        :param df: DataFrame contenente i dati relativi ai docenti.
        :type df: pandas.DataFrame
        :param filename: Nome del file di output (senza estensione).
        :type filename: str
        :raises Exception: Se si verifica un errore durante la scrittura del file.
        """
        # Crea la cartella 'lp' se non esiste
        output_dir = 'lp'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        comment_character = '% '
        # filepath = os.path.join(self.dataset_path, filename + '.lp')
        filepath = os.path.join(output_dir, filename + '.lp')

        # Set per tracciare valori già scritti
        docenti_aggiunti = set()
        ssd_aggiunti = set()
        fascia_aggiunti = set()

        try:
            with open(filepath, 'w') as file:

                # Scrive la sezione dei vari SSD
                file.write(f"{comment_character} SEZIONE: SSD\n")
                for _, row in df.iterrows():
                    # Non posso usare le lettere in maiuscolo perchè possono essere scambiate per variabili e non atomi
                    ssd = row['SSD'].split('/')
                    settore = ssd[0].lower()
                    settore = settore.replace('-', '')
                    numero = int(ssd[1])
                    
                    # ssd = str(ssd)
                    # if ssd not in ssd_aggiunti:
                    if settore not in ssd_aggiunti:
                        file.write(f"ssd({settore}).\n")
                        ssd_aggiunti.add(settore)
                        
                file.write("\n")

                # Scrive la sezione delle fasce dei contratti
                file.write(f"{comment_character} SEZIONE: FASCIE\n")
                for _, row in df.iterrows():
                    fascia = row['Fascia']
                    if 'ricercatore' in fascia.lower():
                        fascia = 'td'
                    else:
                        fascia = 'ti'

                    if fascia not in fascia_aggiunti:
                        file.write(f"fascia({fascia}).\n")
                        fascia_aggiunti.add(fascia)
                file.write("\n")

                # Scrive la sezione dei docenti
                file.write(f"{comment_character} SEZIONE: Docenti\n")
                for _, row in df.iterrows():
                    if not row['Matricola'] or row['Matricola'] is None or row['Matricola'].lower() == 'nan':
                        continue
                    else:
                        matricola_docente = int(float(row['Matricola']))
                    
                    ssd = row['SSD'].split('/')
                    settore = ssd[0].lower()
                    settore = settore.replace('-', '')
                    numero = int(ssd[1])
                    ssd = str(ssd)

                    nome_docente = row['Cognome e Nome']

                    if matricola_docente not in docenti_aggiunti:
                        file.write(f"{comment_character} {nome_docente} ({matricola_docente}), SSD caratterizzante: {settore}/{numero}\n")
                        file.write(f"matricola_docente({matricola_docente}).\n")
                        docenti_aggiunti.add(matricola_docente)
                docenti_aggiunti = set() # reset docenti aggiunti
                file.write("\n")
                
                # Scrive la sezione dei docenti
                file.write(f"{comment_character} SEZIONE: SSD caratterizzante dei docenti\n")
                for _, row in df.iterrows():
                    if not row['Matricola'] or row['Matricola'] is None or row['Matricola'].lower() == 'nan':
                        raise Exception("Matricola non trovata")
                        continue
                    else:
                        matricola_docente = int(float(row['Matricola']))
                    
                    fascia = row['Fascia']
                    if 'ricercatore' in fascia.lower():
                        fascia = 'td'
                    else:
                        fascia = 'ti'

                    ssd = row['SSD'].split('/')
                    settore = ssd[0].lower()
                    settore = settore.replace('-', '')
                    numero = int(ssd[1])
                    ssd = str(ssd)

                    nome_docente = row['Cognome e Nome']

                    if matricola_docente not in docenti_aggiunti:
                        file.write(f"{comment_character} {nome_docente} ({matricola_docente}), SSD caratterizzante: {settore}/{numero}\n")
                        file.write(f"docente({matricola_docente}, {fascia}, {settore}) :- matricola_docente({matricola_docente}), fascia({fascia}), ssd({settore}).\n")
                        docenti_aggiunti.add(matricola_docente)
                file.write("\n")

            print(f"Dati salvati con successo in: {filepath}")
        except Exception as e:
            raise Exception(f"Errore durante il salvataggio dei dati su '{filepath}': {e}")
        
    def scrivi_docenti_a_contratto(self, df, filename):
        """
        Genera un file ASP contenente informazioni sui docenti a contratto.

        :param df: DataFrame contenente i dati relativi ai docenti a contratto.
        :type df: pandas.DataFrame
        :param filename: Nome del file di output (senza estensione).
        :type filename: str
        :raises Exception: Se si verifica un errore durante la scrittura del file.
        """
        SKIP = True

        # Crea la cartella 'lp' se non esiste
        output_dir = 'lp'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        comment_character = '% '
        # filepath = os.path.join(self.dataset_path, filename + '.lp')
        filepath = os.path.join(output_dir, filename + '.lp')

        # Set per tracciare valori già scritti
        docenti_aggiunti = set()

        try:
            with open(filepath, 'w') as file:

                # Scrive la sezione delle fasce dei contratti
                file.write(f"{comment_character} SEZIONE: FASCIE\n")
                file.write(f"fascia(c).\n")
                file.write("\n")

                # Scrive la sezione dei docenti
                file.write(f"{comment_character} SEZIONE: Docenti\n")
                
                if SKIP:
                    file.write(f"jolly(1..5).\n")
                else:
                    for _, row in df.iterrows():
                        if not row['Matricola'] or row['Matricola'] is None or str(row['Matricola']).lower() == 'nan':
                            continue
                        else:
                            matricola_docente = int(float(row['Matricola']))

                        nome_docente = row['Cognome'] + " " + row['Nome']

                        if matricola_docente not in docenti_aggiunti:
                            file.write(f"{comment_character} {nome_docente} ({matricola_docente}), docente a contratto\n")
                            file.write(f"matricola_docente({matricola_docente}).\n")
                            file.write(f"jolly({matricola_docente}).\n")
                            docenti_aggiunti.add(matricola_docente)
                    docenti_aggiunti = set() # reset docenti aggiunti
                    file.write("\n")        

            print(f"Dati salvati con successo in: {filepath}")
        except Exception as e:
            raise Exception(f"Errore durante il salvataggio dei dati su '{filepath}': {e}")