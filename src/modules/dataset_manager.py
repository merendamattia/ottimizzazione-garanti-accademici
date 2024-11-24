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
            if filename.endswith(".lp")
        ]
        return departments

    def load_data(self, filename):
        """
        Legge i dati da un file di testo e li stampa.
        :param filename: Nome del file (senza estensione) da cui leggere i dati.
        :raises FileNotFoundError: Se il file specificato non esiste.
        :raises Exception: Per altri errori durante la lettura del file.
        """
        path = os.path.join(self.dataset_path, f"{filename}.lp")
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

        try:
            with open(filepath, 'w') as file:
                # Scrive la sezione dei tipi di corso
                file.write(f"{comment_character} SEZIONE: Tipi di Corso\n")
                for _, row in df.iterrows():
                    tipoCorso = row['Cod. Tipo Corso']
                    if tipoCorso not in tipi_corso_aggiunti:
                        file.write(f"tipo_corso({tipoCorso}).\n")
                        tipi_corso_aggiunti.add(tipoCorso)
                file.write("\n")

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

                # Scrive la sezione dei docenti
                file.write(f"{comment_character} SEZIONE: Docenti\n")
                for _, row in df.iterrows():
                    matricola = row['Matricola']
                    prof = row['Cognome'] + " " + row['Nome']
                    if matricola not in docenti_aggiunti:
                        file.write(f"{comment_character} {prof} ({matricola})\n")
                        file.write(f"docente({matricola}).\n")
                        docenti_aggiunti.add(matricola)
                file.write("\n")

                # Scrive la sezione dei corsi
                file.write(f"{comment_character} SEZIONE: Corsi\n")
                for _, row in df.iterrows():
                    codiceCorso = row['Cod. Att. Form.']
                    nomeCorso = row['Des. Insegnamento']
                    if codiceCorso not in corsi_aggiunti:
                        file.write(f"{comment_character} {nomeCorso} ({codiceCorso})\n")
                        file.write(f"corso({codiceCorso}).\n")
                        corsi_aggiunti.add(codiceCorso)
                file.write("\n")

                # Scrive le relazioni tra corsi e docenti
                file.write(f"{comment_character} SEZIONE: Relazioni Corsi-Docenti\n")
                for _, row in df.iterrows():
                    codiceCorso = row['Cod. Att. Form.']
                    matricola = row['Matricola']
                    prof = row['Cognome'] + " " + row['Nome']
                    file.write(f"{comment_character} Corso: {codiceCorso}, Docente: {prof}\n")
                    file.write(f"docente_corso(corso({codiceCorso}), docente({matricola})).\n")
                file.write("\n")

                # Scrive le informazioni complete sui corsi
                file.write(f"{comment_character} SEZIONE: Informazioni Corsi\n")
                for _, row in df.iterrows():
                    codiceCorso = row['Cod. Att. Form.']
                    matricola = row['Matricola']
                    cfu = row['CFU']
                    oreCorso = row['Ore']
                    prof = row['Cognome'] + " " + row['Nome']
                    tipoCorso = row['Cod. Tipo Corso']
                    file.write(f"{comment_character} Corso: {codiceCorso} ({tipoCorso}), Docente: {prof}, CFU: {cfu}, Ore: {oreCorso}\n")
                    file.write(f"informazioni_corso(corso({codiceCorso}), tipo_corso({tipoCorso}), docente({matricola}), cfu({cfu}), ore({oreCorso})).\n")

            print(f"Dati salvati con successo in: {filepath}")
        except Exception as e:
            raise Exception(f"Errore durante il salvataggio dei dati su '{filepath}': {e}")