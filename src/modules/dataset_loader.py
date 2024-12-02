import openpyxl
import pandas as pd

class DatasetLoader:
    """
    Classe per la gestione del caricamento, filtraggio e salvataggio dei dati da file Excel o CSV.
    """

    def __init__(self, input_file_path="dataset/coperture.xlsx"):
        """
        Inizializza la classe DatasetLoader con il percorso al dataset.
        :param input_file_path: Path relativo al file Excel da leggere (default: "dataset/coperture.xlsx").
        """
        self.input_file_path = input_file_path
    
    def get_values(self, dataset=None, columns=None):
        """
        Carica un file Excel o utilizza un dataset esistente, filtrando opzionalmente per colonne specifiche.
        :param dataset: DataFrame esistente da utilizzare (default: None). Se None, viene caricato il file Excel.
        :param columns: Lista di colonne da mantenere (esempio: ['Matricola', 'Cognome']).
        :return: DataFrame contenente tutte le righe, filtrato per le colonne specificate (se fornite).
        :raises ImportError: Se il pacchetto openpyxl non è installato.
        :raises KeyError: Se una o più colonne specificate non esistono nel dataset.
        """
        try:

            if dataset is None:
                # Legge l'intero file
                df = pd.read_excel(self.input_file_path, engine="openpyxl")
                df = pd.read_excel(self.input_file_path, sheet_name=0, header=0, usecols=None, nrows=None)
            else:
                df = dataset
            
            # Filtraggio sulle colenne desiderate
            if columns:
                df = df[columns]
                # print(df)
            return df
        except ImportError as e:
            print("Errore: il pacchetto 'openpyxl' non è installato.")
            raise e
        except KeyError as e:
            print(f"Errore: una o più colonne specificate non esistono nel file. {e}")
            raise e
    
    def filter_by_values(self, filters, dataset=None, only_prefix=False):
        """
        Filtra i dati in base a più valori specifici in diverse colonne, convertendo tutti i valori in stringhe.
        :param filters: Dizionario in cui le chiavi sono i nomi delle colonne e i valori sono liste di valori da filtrare.
                        Esempio: {'Cod. Tipo Corso': ['LM'], 'SSD': ['INF/01', 'MAT/05']}.
        :param dataset: DataFrame esistente da utilizzare (default: None). Se None, viene caricato il file Excel.
        :return: DataFrame contenente solo le righe che soddisfano i criteri di filtraggio.
        :raises ImportError: Se il pacchetto openpyxl non è installato.
        :raises KeyError: Se una delle colonne specificate nei filtri non esiste nel dataset.
        :raises Exception: Per altri errori durante il filtraggio.
        """
        try:
            if dataset is None:
                # Carica l'intero dataset
                df = pd.read_excel(self.input_file_path, engine="openpyxl")
            else:
                df = dataset
            
            # Converte tutti i valori del DataFrame in stringhe
            df = df.astype(str)

            # print(f"Filtri: {filters}")
            
            # Applica i filtri
            for column, values in filters.items():
                # Verifica che la colonna esista
                if column not in df.columns:
                    raise KeyError(f"La colonna '{column}' non esiste nel dataset. \nColonne disponibili: {list(df.columns)}")
                
                if only_prefix:
                    # Filtra il DataFrame per i prefissi specificati nella colonna
                    df = df[df[column].str.startswith(tuple(values))]
                    # print(f"Filtrate {df.size} row per '{column}': {values}.")
                else:
                    # Filtra il DataFrame per i valori specificati nella colonna
                    df = df[df[column].isin(map(str, values))]
                    # print(f"Filtrate {df.size} row per '{column}': {values}.")
            
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
    
    
    def df_to_dict(self, df, id_type="col"):
        """
        Converte un DataFrame Pandas in un dizionario strutturato.

        Il dizionario risultante contiene:
        - "rows": lista degli identificativi delle righe (index del DataFrame).
        - "cols": lista degli identificativi delle colonne (header del DataFrame).
        - Chiavi dinamiche: il contenuto delle colonne (default) o delle righe.

        :param df: Un DataFrame Pandas da convertire.
        :type df: pandas.DataFrame
        :param id_type: Tipo di identificatore per il contenuto. "col" per colonne (default),
                        "row" per righe.
        :type id_type: str, optional
        :return: Un dizionario strutturato contenente informazioni su righe, colonne
                 e i dati associati.
        :rtype: dict

        :example:
        input:
            df =
                A   B   C
            0   1   2   3
            1   4   5   6

        output (id_type="col"):
        {
            "rows": [0, 1],
            "cols": ["A", "B", "C"],
            "A": [1, 4],
            "B": [2, 5],
            "C": [3, 6]
        }

        output (id_type="row"):
        {
            "rows": [0, 1],
            "cols": ["A", "B", "C"],
            0: [1, 2, 3],
            1: [4, 5, 6]
        }
        """
        if df is None or df.empty:
            return {}

        result = {
            "rows": df.index.tolist(),
            "cols": df.columns.tolist()
        }

        if id_type == "col":
            for col in df.columns:
                result[col] = df[col].tolist()
        elif id_type == "row":
            for row in df.index:
                result[row] = df.loc[row].tolist()
        else:
            raise ValueError("Il parametro id_type deve essere 'col' o 'row'.")

        return result
    
    def save_to_file(self, df, output_file_path, file_format="csv"):
        """
        Salva il DataFrame su un file specificato.
        :param df: Il DataFrame da salvare.
        :param output_file_path: Percorso del file di output.
        :param file_format: Formato del file, può essere 'csv' o 'excel'.
        :raises ValueError: Se il formato specificato non è 'csv' o 'excel'.
        :raises Exception: Per altri errori durante il salvataggio del file.
        """
        try:
            if file_format == "csv":
                df.to_csv(output_file_path, index=False)
                # print(f"File salvato come CSV in: {output_file_path}")
            elif file_format == "excel":
                df.to_excel(output_file_path, index=False, engine="openpyxl")
                # print(f"File salvato come Excel in: {output_file_path}")
            else:
                raise ValueError("[Errore] Formati supportati: 'csv', 'excel'.")
        except Exception as e:
            print(f"Errore durante il salvataggio del file: {e}")
            raise e
        
