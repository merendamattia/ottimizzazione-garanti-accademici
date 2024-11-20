import os

class Loader:
    def __init__(self, dataset_path="dataset"):
        """
        Inizializza la classe Loader con il percorso della cartella dataset.
        :param dataset_path: Path alla cartella contenente i file di dataset.
        """
        self.dataset_path = dataset_path

    def get_departments(self):
        """
        Ottiene la lista dei dipartimenti basandosi sui file nella cartella dataset.
        :return: Una lista di dipartimenti (nomi file senza estensione).
        """
        if not os.path.exists(self.dataset_path):
            print(f"Errore: la cartella '{self.dataset_path}' non esiste.")
            return []

        departments = [
            os.path.splitext(filename)[0]
            for filename in os.listdir(self.dataset_path)
            if filename.endswith(".txt")
        ]
        return departments

    def load_data(self, filename):
        """
        Legge i dati da un file di testo e li stampa.
        :param filename: Nome del file (senza estensione) da cui leggere i dati.
        """
        path = os.path.join(self.dataset_path, f"{filename}.txt")
        if not os.path.exists(path):
            print(f"Errore: il file '{path}' non esiste.")
            return

        try:
            with open(path, 'r') as file:
                content = file.read().strip()
                print(f"Contenuto di '{path}':")
                print(content)
        except Exception as e:
            print(f"Errore durante la lettura del file '{path}': {e}")