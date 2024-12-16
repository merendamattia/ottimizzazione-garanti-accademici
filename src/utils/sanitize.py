# %%
import pandas as pd
import openpyxl
import re

path_ns_coperture = "../dataset/originali/coperture.xlsx"
path_ns_docenti = "../dataset/originali/docenti.xlsx"
path_ns_elenco_24_25 = "../dataset/originali/elenco_2024-2025.xlsx"

path_coperture = "../dataset/coperture.xlsx"
path_docenti = "../dataset/docenti.xlsx"
path_coperture_contratti = "../dataset/docenti_a_contratto.xlsx"
path_coperture_rimaste = "../dataset/insegnamenti_senza_docente.xlsx"
path_elenco_24_25 = "../dataset/elenco_2024-2025.xlsx"
path_allegato_d = "../dataset/allegato-d-sanitized.xlsx"
path_elenco_allegato = "../dataset/elenco_allegato.xlsx"

def aggiorna_cod_tipo_corso(row, df_allegato):
    """
    Aggiorna il codice del tipo di corso in base alla descrizione del corso.

    La funzione esamina la descrizione del corso e, se corrisponde ad alcune parole chiave specifiche, 
    aggiorna il codice tipo corso (ad esempio 'LT' o 'LM').

    :param row: Una riga del DataFrame contenente le informazioni del corso.
    :type row: pandas.Series
    :return: Il codice tipo corso aggiornato.
    :rtype: str
    :raises ValueError: Se la descrizione del corso non corrisponde a nessuna delle regole mappate.
    """
    # print(df_allegato.columns.tolist())
    # print(row)
    codice_corso_studio = row["Cod. Corso di Studio"]
    tipo_corso = row['Cod. Tipo Corso']
    
    tipo_corso = tipo_corso.lower()
    if tipo_corso in ["lm6", "lm5"]:
        return tipo_corso.upper()

    filtro = df_allegato["CODICE U-GOV"] == codice_corso_studio
    corrispondenza = df_allegato[filtro]
    
    if not corrispondenza.empty:
        # Se c'è corrispondenza, prendi il valore di "Cod. Tipo laurea"
        nuovo_tipo_corso = corrispondenza.iloc[0]["Cod. Tipo laurea"]
        return nuovo_tipo_corso.upper()
    return tipo_corso.upper()

def sanitize_codici_corso(df):
    """
    Sanifica i codici dei corsi in base alla descrizione e al tipo del corso.

    La funzione sostituisce "L" con "LT" per uniformare il tipo di corso e applica le regole di 
    aggiornamento tramite la funzione `aggiorna_cod_tipo_corso`.

    :param df: DataFrame contenente le informazioni dei corsi.
    :type df: pandas.DataFrame
    :return: DataFrame con i codici tipo corso aggiornati.
    :rtype: pandas.DataFrame
    """
    
    # Sostituzione l con lt
    df.loc[df["Cod. Tipo Corso"].str.lower() == "l", "Cod. Tipo Corso"] = "LT"

    df_allegato = pd.read_excel(path_elenco_allegato, engine="openpyxl", dtype=str)
    df["Cod. Tipo Corso"] = df.apply(lambda row: aggiorna_cod_tipo_corso(row, df_allegato), axis=1)
    
    
    return df


# %%
def sanitize_coperture():
    """
    Sanifica i dati di copertura, rimuovendo le righe con matricola vuota e 
    mantenendo solo i record con matricole esistenti nel file dei docenti.

    La funzione esegue le seguenti operazioni:
    1. Carica i dati dal file `path_ns_coperture`.
    2. Rimuove le righe in cui il campo "Matricola" è vuoto.
    3. Converte la "Matricola" in formato stringa.
    4. Filtra i dati mantenendo solo le matricole esistenti nel file dei docenti.
    5. Sanifica il campo "Cod. Tipo Corso" tramite la funzione `sanitize_codici_corso`.
    6. Salva i dati sanificati nel file `path_coperture`.

    :return: Nessuno. I dati sanificati vengono salvati nel file di output.
    :rtype: None
    """
    df = pd.read_excel(path_ns_coperture, engine="openpyxl", dtype=str)
    # print(df)
    # Rimuovere le righe che hanno il campo matricola vuoto
    df = df.dropna(subset=["Matricola"])
    # print(df)
    df["Matricola"] = df["Matricola"].astype(int)
    # print(df)
    df["Matricola"] = df["Matricola"].astype(str)
    # astype
    matricole = pd.read_excel(path_docenti, engine="openpyxl", dtype=str)["Matricola"]
    # print(matricole)
    df = df[df["Matricola"].isin(matricole)]
    df = sanitize_codici_corso(df)
    
    df.to_excel(path_coperture, index=False)


# %%
def sanitize_docenti():
    """
    Sanifica i dati dei docenti, rimuovendo eventuali caratteri non numerici dalle matricole 
    e salvando i risultati nel file di output.

    La funzione rimuove i caratteri `.` e `,` dalle matricole e converte il campo in formato stringa 
    prima di salvare il DataFrame nel file Excel `path_docenti`.

    :return: Nessuno. I dati dei docenti sanificati vengono salvati nel file di output.
    :rtype: None
    """
    df = pd.read_excel(path_ns_docenti, engine="openpyxl", dtype=str)
    # rimozioni .
    df["Matricola"] = df["Matricola"].str.replace(".", "")
    # rimozioni ,
    df["Matricola"] = df["Matricola"].str.replace(",", "")
    
    # print(df)
    df["Matricola"] = df["Matricola"].astype(int)
    df["Matricola"] = df["Matricola"].astype(str)
    # salvataggio
    df.to_excel(path_docenti, index=False)
    
    
# %%    
def compute_extra_data():
    """
    Calcola i dati extra per i corsi senza docenti e li salva nel file di output.

    La funzione esegue le seguenti operazioni:
    1. Carica i dati dal file `path_ns_coperture`.
    2. Rimuove le righe in cui il campo "Matricola" è vuoto.
    3. Converte la "Matricola" in formato stringa.
    4. Filtra i dati mantenendo solo i record con matricole che non esistono nel file dei docenti.
    5. Sanifica il campo "Cod. Tipo Corso" tramite la funzione `sanitize_codici_corso`.
    6. Salva i dati nel file `path_coperture_contratti`.

    :return: Nessuno. I dati vengono salvati nel file di output.
    :rtype: None
    """
    df = pd.read_excel(path_ns_coperture, engine="openpyxl", dtype=str)
    # print(df)
    # Rimuovere le righe che hanno il campo matricola vuoto
    df = df.dropna(subset=["Matricola"])
    # print(df)
    df["Matricola"] = df["Matricola"].astype(int)
    # print(df)
    df["Matricola"] = df["Matricola"].astype(str)
    # astype
    matricole = pd.read_excel(path_docenti, engine="openpyxl", dtype=str)["Matricola"]
    # print(matricole)
    
    # Not isin
    df = df[~df["Matricola"].isin(matricole)]
    
    df = sanitize_codici_corso(df)
    
    df.to_excel(path_coperture_contratti, index=False)
    
# %%%
def compute_remained():
    """
    Calcola i corsi rimasti senza docente e li salva nel file di output.

    La funzione esegue le seguenti operazioni:
    1. Carica i dati completi dal file `path_ns_coperture`, quelli già assegnati ai docenti dal file `path_coperture`,
       e quelli assegnati a contratti dal file `path_coperture_contratti`.
    2. Esclude i corsi già assegnati a docenti (sia determinati che a contratto) dal set di corsi completi.
    3. Rimuove le righe con valori vuoti in tutte le colonne.
    4. Salva i corsi rimasti nel file `path_coperture_rimaste`.

    :return: Nessuno. I dati dei corsi rimasti vengono salvati nel file di output.
    :rtype: None
    """
    df_full = pd.read_excel(path_ns_coperture, engine="openpyxl", dtype=str)
    df_indeterminati = pd.read_excel(path_coperture, engine="openpyxl", dtype=str)
    df_contratti = pd.read_excel(path_coperture_contratti, engine="openpyxl", dtype=str)

    
    df_full = df_full[~df_full["Cod. Att. Form."].isin(df_indeterminati["Cod. Att. Form."])]
    df_full = df_full[~df_full["Cod. Att. Form."].isin(df_contratti["Cod. Att. Form."])]

    df_full.dropna(how="all", inplace=True)
    df_full.to_excel(path_coperture_rimaste, index=False)
    


def sanitize_elenco_24_25():
    df = pd.read_excel(path_ns_elenco_24_25, engine="openpyxl", dtype=str)
    # tiene solo le righe che hanno la colonna "NOTE" vuota
    df = df[df["NOTE"].isna()]
    df.to_excel(path_elenco_24_25, index=False)
    print("Elenco 24-25 sanitizzato")

def merge_elenco_allegato():
    # legge il contenuto della colonna classe di df_allegato e il contenuto della cella (in lower cases) è contenuto nella
    # colonna classe di df_elenco aggiunge alla riga di df_elenco il contenuto delle colonne Tipo laurea, N. di riferimento e
    # N. max a df_elenco
    df_elenco = pd.read_excel(path_elenco_24_25, engine="openpyxl", dtype=str)
    df_allegato = pd.read_excel(path_allegato_d, engine="openpyxl", dtype=str)
    
    df_elenco = df_elenco.drop(columns=["NOTE"])
    df_elenco["CLASSE"] = df_elenco["CLASSE"].str.lower()
    df_allegato["CLASSE"] = df_allegato["CLASSE"].str.lower()
    
    for _, row in df_allegato.iterrows():
        classe_allegato = row["CLASSE"]
        mask = df_elenco["CLASSE"].str.contains(classe_allegato, na=False, regex=False)

        df_elenco.loc[mask, "Cod. Tipo laurea"] = row.get("Tipo laurea", "")
        # questi sono interi 
        df_elenco.loc[mask, "N. di riferimento"] = row.get("N. di riferimento", "")
        df_elenco.loc[mask, "N. max"] = row.get("N. max", "")
    
    # aggiorna df_elenco
    
    # gestione delle lauree (casi particolari)
    # se nella colonna "DOCENZA DI RIFERIMENTO" è vuota non fare nulla
    # se nella colonna "DOCENZA DI RIFERIMENTO" sono presenti i numeri 5 - 3 imposta il contenuto della colonna Cod. Tipo Laurea = LCPA
    # se nella colonna "DOCENZA DI RIFERIMENTO" sono presenti i numeri 4 - 2 imposta il contenuto della colonna Cod. Tipo Laurea = LCPB
    # se nella colonna "DOCENZA DI RIFERIMENTO" sono presenti i numeri 3 - 1 imposta il contenuto della colonna Cod. Tipo Laurea = LCPC
    # deve essere fatto tramite regex perché il contenuto della cella è "5  DI CUI 3 PO/PA"
    
    def codifica_tipo_laurea(docenza):
        """Ritorna il codice Cod. Tipo Laurea in base al contenuto della colonna DOCENZA DI RIFERIMENTO."""
        if pd.isna(docenza):
            return None
        docenza = str(docenza)
        if re.search(r"\b5\b.*\b3\b", docenza):
            # Laurea caso particolare A
            return "LCPA"
        elif re.search(r"\b4\b.*\b2\b", docenza):
            # Laurea caso particolare B
            return "LCPB"
        elif re.search(r"\b3\b.*\b1\b", docenza):
            # Laurea caso particolare C
            return "LCPC"
        return None
    
    df_elenco["Cod. Tipo laurea"] = df_elenco.apply(
        lambda row: codifica_tipo_laurea(row["DOCENZA DI RIFERIMENTO"]) or row["Cod. Tipo laurea"], axis=1
    )
    
    df_elenco.to_excel(path_elenco_allegato, index=False)
    print("Elenco-allegato 24-25 sanitizzato")
    # return df_elenco

# %%
def sanitize():
    """
    Funzione principale per sanificare i dati.

    La funzione chiama tutte le operazioni di sanificazione:
    - Sanifica i dati dei docenti.
    - Sanifica i dati delle coperture.
    - Calcola i dati extra per i corsi senza docenti.
    - Calcola i corsi rimasti senza docente.

    :return: Nessuno. Vengono salvati i dati nei rispettivi file di output.
    :rtype: None
    """
    sanitize_elenco_24_25()
    merge_elenco_allegato()
    sanitize_docenti()
    sanitize_coperture()
    compute_extra_data()
    compute_remained()

# %%
if __name__ == "__main__":
    sanitize()
    
# %%
