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

def aggiorna_cod_tipo_corso(row):
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
    descrizione = row['Des. Corso di Studio']
    tipo_corso = row['Cod. Tipo Corso']
    descrizione = descrizione.lower()
    tipo_corso = tipo_corso.lower()

    # TODO aggiungere LT a orient. profess.
    # Regole di aggiornamento
    if re.search(r'(?i)(?=.*serviz)(?=.*social)', descrizione):
        if tipo_corso == 'lt':
            return 'LTSS'
        elif tipo_corso == 'lm':
            return 'LMSS'
    elif 'professione sanitaria' in descrizione and tipo_corso == 'lt':
        return 'LTPS'
    
    # elif 'professione sanitaria' in descrizione and tipo_corso == 'lt':
    #     return 'LTPS'
    
    elif 'infermieristic' in descrizione and tipo_corso == 'lm':
        return 'LMI'
    
    elif re.search(r'(?i)(?=.*scienz)(?=.*motor)', descrizione):
        if tipo_corso == 'lt':
            return 'LTSM'
        elif tipo_corso == 'lm':
            return 'LMSM'
    
    raise ValueError(f"Valore non mappato: {descrizione.lower()}, {tipo_corso.lower()}")


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
    
    stringhe_da_cercare = ["professione sanitaria", "scienze motorie", "infermieristic"]
    
    regex = "|".join(stringhe_da_cercare)
    regex_ss = r'(?i)(?=.*serviz)(?=.*social)'
    regex_sm = r'(?i)(?=.*scienz)(?=.*motor)'
    
    filtered_df = df[
        (df["Des. Corso di Studio"].str.contains(regex, na=False, flags=re.IGNORECASE)) |
        (df["Des. Corso di Studio"].str.contains(regex_ss, na=False, flags=re.IGNORECASE)) |
        (df["Des. Corso di Studio"].str.contains(regex_sm, na=False, flags=re.IGNORECASE))
    ]
    
    filtered_df["Cod. Tipo Corso"] = filtered_df.apply(aggiorna_cod_tipo_corso, axis=1)
    
    keys = ["Cod. Corso di Studio", "Cod. Tipo Corso"]
    
    filtered_df = filtered_df[keys].drop_duplicates(subset=['Cod. Corso di Studio'])
    
    # filtered_df.to_csv('filtered_data.csv', index=False)
    
    mapping = filtered_df.set_index("Cod. Corso di Studio")["Cod. Tipo Corso"].to_dict()
    
    # print(mapping)
    
    df["Cod. Tipo Corso"] = df["Cod. Corso di Studio"].map(mapping).fillna(df["Cod. Tipo Corso"])
    
    return df
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
    sanitize_docenti()
    sanitize_coperture()
    compute_extra_data()
    compute_remained()

# %%
if __name__ == "__main__":
    # sanitize()
    sanitize_elenco_24_25()
# %%
