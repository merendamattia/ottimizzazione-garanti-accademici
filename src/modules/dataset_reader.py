import openpyxl
import pandas as pd

class DatasetReader:
    def __init__(self, input_file_path="dataset"):
        """
        Inizializza la classe DatasetReader con il percorso al datset.
        :param input_file_path: Path relativo al file da leggere.
        """
        self.input_file_path = input_file_path
    
    def get_from_excel(self, columns=None):
        """
        Carica un file Excel e filtra per colonne specifiche se fornito.
        :param columns: Lista di colonne da mantenere (es. ["Matricola", "SSD 2015"]).
        :return: DataFrame filtrato.
        """
        try:
            # Legge l'intero file
            df = pd.read_excel(self.input_file_path, engine="openpyxl")
            df = pd.read_excel(self.input_file_path, sheet_name=0, header=0, usecols=None, nrows=None)
            
            # Filtraggio sulle colenne desiderate
            if columns:
                df = df[columns]
                print(df)
            return df
        except ImportError as e:
            print("Errore: il pacchetto 'openpyxl' non è installato.")
            raise e
        except KeyError as e:
            print(f"Errore: una o più colonne specificate non esistono nel file. {e}")
            raise e
    
    def save_to_file(self, df, output_file_path, file_format="csv"):
        """
        Salva il DataFrame su un file specificato.
        :param df: Il DataFrame da salvare.
        :param output_file_path: Percorso del file di output.
        :param file_format: Formato del file, può essere 'csv' o 'excel'.
        """
        try:
            if file_format == "csv":
                df.to_csv(output_file_path, index=False)
                print(f"File salvato come CSV in: {output_file_path}")
            elif file_format == "excel":
                df.to_excel(output_file_path, index=False, engine="openpyxl")
                print(f"File salvato come Excel in: {output_file_path}")
            else:
                raise ValueError("Formato non supportato. Usa 'csv' o 'excel'.")
        except Exception as e:
            print(f"Errore durante il salvataggio del file: {e}")
            raise e
