import openpyxl
import pandas as pd

class DatasetLoader:
    def __init__(self, input_file_path="dataset/coperture.xlsx"):
        """
        Inizializza la classe DatasetLoader con il percorso al datset.
        :param input_file_path: Path relativo al file da leggere.
        """
        self.input_file_path = input_file_path
    
    def get_from_database(self, columns=None):
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
    
    def filter_by_values(self, filters):
        """
        Filtra i dati in base a più valori specifici in diverse colonne, convertendo tutti i valori in stringhe.
        :param filters: Dizionario in cui le chiavi sono i nomi delle colonne e i valori sono liste di valori da filtrare.
                        Esempio: {'Cod. Tipo Corso': ['LM'], 'SSD': ['INF/01', 'MAT/05']}
        :return: DataFrame filtrato.
        """
        try:
            # Carica l'intero dataset
            df = pd.read_excel(self.input_file_path, engine="openpyxl")
            
            # Converte tutti i valori del DataFrame in stringhe
            df = df.astype(str)

            print(f"Filtri: {filters}")
            
            # Applica i filtri
            for column, values in filters.items():
                # Verifica che la colonna esista
                if column not in df.columns:
                    raise KeyError(f"La colonna '{column}' non esiste nel dataset. \nColonne disponibili: {list(df.columns)}")
                
                # Filtra il DataFrame per i valori specificati nella colonna
                df = df[df[column].isin(map(str, values))]
                print(f"Filtrate {df.size} row per '{column}': {values}.")
            
            return df
        except ImportError as e:
            print("Errore: il pacchetto 'openpyxl' non è installato.")
            raise e
        except KeyError as e:
            print(f"Errore: {e}")
            raise e
        except Exception as e:
            print(f"Errore durante il filtraggio dei dati: {e}")
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
                raise ValueError("[Errore] Formati supportati: 'csv', 'excel'.")
        except Exception as e:
            print(f"Errore durante il salvataggio del file: {e}")
            raise e
        
