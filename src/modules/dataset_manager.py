import os

class DatasetManager:
    """
    Classe per la gestione di file di dataset e la generazione di file ASP strutturati.
    """

    def __init__(self, dataset_path="dataset/"):
        """
        Inizializza la classe DatasetManager con il percorso della cartella contenente i file di dataset.
        :param dataset_path: Path alla cartella contenente i file di dataset (default: "dataset/").
        """
        self.dataset_path = dataset_path

    def get_departments(self):
        """
        Ottiene la lista dei dipartimenti basandosi sui file presenti nella cartella del dataset.
        :return: Una lista di dipartimenti (nomi dei file senza estensione).
        :raises FileNotFoundError: Se la cartella del dataset non esiste.
        """
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Errore: la cartella '{self.dataset_path}' non esiste.")

        departments = [
            os.path.splitext(filename)[0]
            for filename in os.listdir(self.dataset_path)
            if filename.endswith(".csv")
        ]
        return departments
    
    def get_sectors(self, SSD = None):
        """
        Ottiene la lista dei settori partendo da una lista di SSD.

        Ogni SSD è rappresentato nel formato "SETTORE/CODICE". Questa funzione estrae
        e restituisce solo la parte relativa al settore (prima del separatore '/').
        
        :param SSD: Una lista di stringhe rappresentanti i SSD. Ad esempio, ["INF/01", "MAT/03"].
        :type SSD: list[str], optional
        :return: Un set di settori se la lista passata come parametro è non vuota. 
                Ritorna un set vuoto se il parametro è None o vuoto.
        :rtype: set[str]

        :example:
        input: ["INF/01", "MAT/03", "FIS/07"]
        output: {"INF", "MAT", "FIS"}
        """
        if SSD:
            # print(SSD)
            items = set()
            for code in SSD:
                # Escludere None, NaN, o stringhe vuote
                if not code or not isinstance(code, str) or code.strip().lower() == 'nan':
                    continue
                # Estrae la parte prima di `/` per ogni elemento della lista
                spl = code.split('/')
                if len(spl) > 1:
                    items.add(spl[0])
            return items
        else:
            return set()
        
    def load_data(self, filename):
        """
        Legge i dati da un file di testo e li stampa.
        :param filename: Nome del file (senza estensione) da cui leggere i dati.
        :raises FileNotFoundError: Se il file specificato non esiste.
        :raises Exception: Per altri errori durante la lettura del file.
        """
        path = os.path.join(self.dataset_path, f'{filename}.csv')
        if not os.path.exists(path):
            raise FileNotFoundError(f"Errore: il file '{path}' non esiste.")

        try:
            with open(path, 'r') as file:
                content = file.read().strip()
                print(f"Contenuto di '{path}':")
                print(content)
        except Exception as e:
            raise Exception(f"Errore durante la lettura del file '{path}': {e}")

    def write_atoms(self, df, filename):
        """
        Scrive i dati del DataFrame in un file ASP (.lp), organizzandoli per sezioni con eliminazione di duplicati.
        :param df: DataFrame contenente i dati da salvare.
        :param filename: Nome del file di output (senza estensione).
        :raises Exception: Per errori durante la scrittura del file.
        """
        comment_character = '% '
        filepath = os.path.join(self.dataset_path, filename + '.lp')

        # Set per tracciare valori già scritti
        cfu_aggiunti = set()
        ore_aggiunte = set()
        docenti_aggiunti = set()
        corsi_aggiunti = set()
        tipi_corso_aggiunti = set()
        ssd_aggiunti = set()

        try:
            with open(filepath, 'w') as file:
                # Scrive la sezione dei tipi di corso
                file.write(f"{comment_character} SEZIONE: Tipi di Corso\n")
                for _, row in df.iterrows():
                    # Non posso usare le lettere in maiuscolo perchè possono essere scambiate per variabili e non atomi
                    tipoCorso = row['Cod. Tipo Corso'].lower()
                    if tipoCorso not in tipi_corso_aggiunti:
                        file.write(f"laurea({tipoCorso}).\n")
                        tipi_corso_aggiunti.add(tipoCorso)
                file.write("\n")

                # Scrive la sezione dei vari SSD
                file.write(f"{comment_character} SEZIONE: SSD\n")
                for _, row in df.iterrows():
                    # Non posso usare le lettere in maiuscolo perchè possono essere scambiate per variabili e non atomi
                    ssd = row['SSD'].split('/')
                    ssd = ssd[0].lower()
                    if ssd not in ssd_aggiunti:
                        file.write(f"ssd({ssd}).\n")
                        ssd_aggiunti.add(ssd)
                file.write("\n")

                """
                # Scrive la sezione dei CFU
                file.write(f"{comment_character} SEZIONE: CFU\n")
                for _, row in df.iterrows():
                    cfu = row['CFU']
                    if cfu not in cfu_aggiunti:
                        file.write(f"cfu({cfu}).\n")
                        cfu_aggiunti.add(cfu)
                file.write("\n")

                # Scrive la sezione delle ore
                file.write(f"{comment_character} SEZIONE: Ore\n")
                for _, row in df.iterrows():
                    oreCorso = row['Ore']
                    if oreCorso not in ore_aggiunte:
                        file.write(f"ore({oreCorso}).\n")
                        ore_aggiunte.add(oreCorso)
                file.write("\n")
                """

                # Scrive la sezione dei docenti
                file.write(f"{comment_character} SEZIONE: Docenti\n")
                for _, row in df.iterrows():
                    if row['Matricola'].lower() == 'nan':
                        matricola_docente = row['Matricola']
                    else:
                        matricola_docente = int(float(row['Matricola']))

                    nome_docente = row['Cognome'] + " " + row['Nome']
                    if matricola_docente not in docenti_aggiunti:
                        file.write(f"{comment_character} {nome_docente} ({matricola_docente})\n")
                        file.write(f"matricola_docente({matricola_docente}).\n")
                        docenti_aggiunti.add(matricola_docente)
                file.write("\n")

                # Scrive la sezione dei corsi
                file.write(f"{comment_character} SEZIONE: Corsi\n")
                for _, row in df.iterrows():
                    matricola_corso = row['Cod. Att. Form.']
                    nome_corso = row['Des. Insegnamento']
                    if matricola_corso not in corsi_aggiunti:
                        file.write(f"{comment_character} {nome_corso} ({matricola_corso})\n")
                        file.write(f"matricola_corso({matricola_corso}).\n")
                        corsi_aggiunti.add(matricola_corso)
                file.write("\n")

                # Scrive le relazioni tra corsi e docenti
                file.write(f"{comment_character} SEZIONE: Relazioni Corsi-Docenti\n")
                for _, row in df.iterrows():
                    if row['Matricola'].lower() == 'nan':
                        matricola_docente = row['Matricola']
                    else:
                        matricola_docente = int(float(row['Matricola']))

                    matricola_corso = row['Cod. Att. Form.']
                    nome_docente = row['Cognome'] + " " + row['Nome']
                    file.write(f"{comment_character} Corso: {matricola_corso}, Docente: {nome_docente}\n")
                    file.write(f"docente_corso({matricola_corso}, {matricola_docente}) :- matricola_corso({matricola_corso}), matricola_docente({matricola_docente}).\n")
                file.write("\n")

                # Scrive le informazioni complete sui corsi
                file.write(f"{comment_character} SEZIONE: Informazioni Corsi\n")
                for _, row in df.iterrows():
                    matricola_corso = row['Cod. Att. Form.']
                    prof = row['Cognome'] + " " + row['Nome']
                    tipoCorso = row['Cod. Tipo Corso'].lower()
                    ssd = row['SSD'].split('/')
                    ssd = ssd[0].lower()
                    file.write(f"{comment_character} Corso: {matricola_corso} ({tipoCorso}), Docente: {prof}\n")
                    file.write(f"corso({matricola_corso}, {tipoCorso}, {ssd}) :- matricola_corso({matricola_corso}), laurea({tipoCorso}), ssd({ssd}).\n")

            print(f"Dati salvati con successo in: {filepath}")
        except Exception as e:
            raise Exception(f"Errore durante il salvataggio dei dati su '{filepath}': {e}")