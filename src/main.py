from modules.dataset_manager import DatasetManager
from modules.course_parser import CourseParser
from modules.dataset_loader import DatasetLoader
import os
import pandas as pd
from fuzzywuzzy import process, fuzz



############################## VARIABILI GLOBALI #################################

# Percorso del file contenente i dati sulle coperture
path_coperture = "dataset/coperture.xlsx"

# Percorso del file contenente i dati dei docenti
path_docenti = "dataset/docenti.xlsx"

# Percorso del file contenente i dati dei docenti a contratto
path_docenti_a_contratto = "dataset/docenti_a_contratto.xlsx"

# Elenco dei file contenenti i dati degli immatricolati (LT, LM, CU)
paths_immatricolati = ["dataset/immatricolati/LT.xlsx", "dataset/immatricolati/LM.xlsx", "dataset/immatricolati/CU.xlsx"]


# Percorso del file contenente l'elenco dei corsi con i rispettivi massimi teorici
path_elenco_allegato = "dataset/elenco_allegato.xlsx"

# Numero minimo di insegnamenti richiesti per considerare valido un corso
NUMERO_MINIMO_DI_INSEGNAMENTI = 9


###################################### FUNZIONI PRINCIPALI ######################################

def init_matricole(filename):
    """
    Carica e salva le matricole dei docenti non a contratto.
    
    Questa funzione:
    1. Carica le matricole dei docenti dal file `path_docenti`.
    2. Rimuove i duplicati e le salva.
    3. Carica i dati dalle coperture e filtra in base alle matricole dei docenti.
    4. Salva i dati filtrati nel file specificato da `filename`.
    
    Args:
        filename (str): Nome del file di output dove salvare le matricole dei docenti.
    
    :return: None
    :rtype: None
    """
    dsl = DatasetLoader(path_docenti)
    
    # Prende le matricole dei docenti non a contratto rimuovendo possibili duplicati
    matricole = dsl.get_values(columns=["Matricola"]).drop_duplicates()["Matricola"].tolist()
    
    dsl = DatasetLoader(path_coperture)
    ds = dsl.get_values(columns=["Cod. Corso di Studio", "Matricola"])
    
    # Filra gli insegnamenti per le matricole dei prof
    ds_min = dsl.filter_by_values(dataset=ds, filters={"Matricola" : matricole})
    
    dsl.save_to_file(ds_min, filename)
    
def init_corsi(filename):
    """
    Inizializza e salva un file con i codici e le descrizioni dei corsi.
    
    Questa funzione:
    1. Carica i dati delle coperture.
    2. Crea una colonna "Overview" che unisce la descrizione del corso e il tipo di corso.
    3. Estrae i codici dei corsi e rimuove i duplicati.
    4. Filtra i corsi sulla base dei codici unici e salva i risultati nel file specificato.
    
    Args:
        filename (str): Nome del file di output dove salvare i codici dei corsi.
    
    :return: None
    :rtype: None
    """
    dsl = DatasetLoader(path_coperture)
    
    df = dsl.get_values(columns=["Cod. Corso di Studio", "Des. Corso di Studio", "Cod. Tipo Corso"])
    
    df["Overview"] = df["Des. Corso di Studio"].astype(str).str.lower() + "(" + df["Cod. Tipo Corso"] + ")"
    
    df = dsl.get_values(dataset=df, columns=["Cod. Corso di Studio", "Overview"])
    
    # Estrae i codici rimuovendo i duplicati
    codici_corsi = dsl.get_values(dataset=df, columns=["Cod. Corso di Studio"]).drop_duplicates()
    
    ds_min = dsl.filter_by_values(dataset=df, filters={"Cod. Corso di Studio" : codici_corsi["Cod. Corso di Studio"].tolist()})
    dsl.save_to_file(ds_min, filename)

def init_corsi_matricole(filepathCorsi, filepathProf):
    """
    Inizializza i file relativi ai corsi e alle matricole.

    Questa funzione:
    1. Inizializza e salva i dati relativi ai corsi e alle matricole.
    2. Se i file di output non esistono, li crea e li salva.
    3. Visualizza un messaggio di completamento e termina l'esecuzione.

    Args:
        filepathCorsi (str): Percorso del file di output per i corsi.
        filepathProf (str): Percorso del file di output per le matricole.
    
    :return: Nessuno. Il programma termina dopo l'esecuzione.
    :rtype: None
    """
    init_corsi(filepathCorsi)
    init_matricole(filepathProf)
    print("Estrazione completata. Rieseguire il programma.")
    exit()



def clean_text(text):
    return text.lower().strip().replace("'", "").replace("à", "a").replace("è", "e").replace("é", "e").replace("ì", "i").replace("ò", "o").replace("ù", "u")

def main():
    """
    Funzione principale per l'elaborazione e la gestione dei dati.

    La funzione esegue le seguenti operazioni:
    1. Inizializza i dataset dei corsi e delle matricole se non esistono.
    2. Filtra e salva i dati dei corsi, docenti e coperture.
    3. Genera i file richiesti in base ai parametri specificati (corsi, docenti, coperture, immatricolati).
    
    - Crea e gestisce i filtri per i corsi in base ai parametri di input.
    - Gestisce i file di dati e li salva nella struttura appropriata.
    
    :return: Nessuno. Il flusso di elaborazione termina.
    :rtype: None
    """
    dataset_dir = 'dataset/corsi/'
    filepathCorsi = dataset_dir + 'codici-corsi.csv'
    filepathProf = dataset_dir + 'codici-matricole.csv'
    
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)
    if not os.path.exists(filepathCorsi) or not os.path.exists(filepathProf):
        init_corsi_matricole(filepathCorsi, filepathProf)
    
    # Inizializza il Dataset Manager
    dataset_manager = DatasetManager(dataset_path=filepathCorsi)

    # Ottiene la lista dei dipartimenti
    courses = dataset_manager.get_courses()

    parser = CourseParser()
    parser.add_courses(courses)
    args = parser.parse()
    
    filters_corsi = {"Cod. Corso di Studio" : list()}
    
    if args.all:
        for key in courses.keys():
            filters_corsi["Cod. Corso di Studio"].append(key)
    else:
        for key in courses.keys():
            if getattr(args, key, False):
                filters_corsi["Cod. Corso di Studio"].append(key)

    filters_corsi ["Cod. Corso di Studio"] = list(set(filters_corsi ["Cod. Corso di Studio"]))
    
    dsl = DatasetLoader(path_coperture)
    df_tmp = dsl.filter_by_values(filters=filters_corsi, only_prefix=False)
    
    # Raggruppa per codice corso e conta le occorrenze
    conteggi = df_tmp['Cod. Corso di Studio'].value_counts()

    # Filtra il DataFrame mantenendo solo i codici corso con almeno 9 occorrenze
    codici_non_validi = conteggi[conteggi <= NUMERO_MINIMO_DI_INSEGNAMENTI].index
    df_tmp = df_tmp[df_tmp['Cod. Corso di Studio'].isin(codici_non_validi)]
    
    excluded = set(df_tmp["Cod. Corso di Studio"].unique())
    
    filters_corsi ["Cod. Corso di Studio"] = list(set(filters_corsi ["Cod. Corso di Studio"]) - excluded)
    
    # Esclusione manuale dei corsi che con richiedo garanti al 50% per funzionare
    hand_exluded = set(["5079", "5080"])
    filters_corsi ["Cod. Corso di Studio"] = list(set(filters_corsi ["Cod. Corso di Studio"]) - hand_exluded)
    
    if not any(vars(args).values()):
        print("Errore: nessun dipartimento selezionato.")
        parser.parser.print_help()
        exit()
    
    filters_docenti = {"Matricola": list()}
    
    dataset_manager = DatasetManager(dataset_path=filepathProf)
    profs = dataset_manager.get_professors()
    
    for code in filters_corsi["Cod. Corso di Studio"]:
        if profs[code]:
            for p in profs[code]:
                filters_docenti["Matricola"].append(p)
                
    filters_docenti ["Matricola"] = list(set(filters_docenti ["Matricola"]))
    
    ### SCRITTURA DOCENTI 
    dataset_loader = DatasetLoader(path_docenti)
    data = dataset_loader.filter_by_values(filters=filters_docenti, only_prefix=False)
    dataset_manager = DatasetManager()
    dataset_manager.scrivi_docenti(data, 'docenti')

    ### SCRITTURA CORSI
    dataset_loader = DatasetLoader(path_coperture)
    data = dataset_loader.filter_by_values(filters=filters_corsi, only_prefix=True)
    dataset_manager = DatasetManager()
    dataset_manager.scrivi_coperture(data, 'coperture')

    ### SCRITTURA DOCENTI A CONTRATTO
    dataset_loader = DatasetLoader(path_docenti_a_contratto)
    data = dataset_loader.get_values()
    dataset_manager = DatasetManager()
    dataset_manager.scrivi_docenti_a_contratto(data, 'docenti_a_contratto')
    
    ### SCRITTURA MINISTERIALE
    dataset_loader = DatasetLoader(path_coperture)
    data = dataset_loader.filter_by_values(filters=filters_corsi, only_prefix=True)
    data = data[["Cod. Corso di Studio", "Cod. Tipo Corso"]].drop_duplicates()
    
    # TODO aggiungere scrittura presidenti corsi di laurea
    ### SCRITTURA PRESIDENTI -> preferenza
    dsl_coperture = DatasetLoader(path_coperture)
    dsl_allegato = DatasetLoader(path_elenco_allegato)
    
    
    
    dsc = dsl_coperture.filter_by_values(filters=filters_corsi, only_prefix=True)
    dsc = dsc[["Cod. Corso di Studio", "Cognome", "Nome", "Matricola"]]
    
    dsc["Nome e Cognome"] = dsc["Nome"].apply(clean_text) + " " + dsc["Cognome"].apply(clean_text)
    filter_corsi2  = dict()
    filter_corsi2["CODICE U-GOV"] = filters_corsi["Cod. Corso di Studio"]
    dsa = dsl_allegato.filter_by_values(filters=filter_corsi2, only_prefix=True)
    dsa = dsa[["CODICE U-GOV", "PRESIDENTE"]]
    dsa["PRESIDENTE"] = dsa["PRESIDENTE"].apply(clean_text)
    
    def most_similar(name, choices, scorer, threshold=90):
        """
        Effettua il fuzzy matching tra una stringa e una lista di scelte.
        Restituisce la corrispondenza migliore se supera la soglia.
        """
        best_match, score = process.extractOne(name, choices, scorer=scorer)
        if score >= threshold:
            return best_match
        # se non c'è match ritorna none
        return None
    
    #TODO merge dei due df basandosi su "CODICE U-GOV" e "Cod. Corso di Studio"
    merged_df = dsc.merge(
        dsa,
        how="left",
        left_on="Cod. Corso di Studio",
        right_on="CODICE U-GOV"
    )
    merged_df.to_excel("merged_df.xlsx", index = False)
    
    #TODO scartare le righe che non hanno un match al 60% tra il valore "Nome e Cognome" e "PRESIDENTE"
    
    merged_df["Match PRESIDENTE"] = merged_df.apply(
        lambda row: most_similar(row["Nome e Cognome"], [row["PRESIDENTE"]], fuzz.token_sort_ratio, threshold=60)
        if pd.notna(row["PRESIDENTE"]) and pd.notna(row["Nome e Cognome"]) else None,
        axis=1
    )
    filtered_df = merged_df[merged_df["Match PRESIDENTE"].notna()]
    filtered_df.to_excel("presidenti.xlsx", index=False)

    # dsc["Match presidente"] = dsc["Nome e Cognome"].apply(
    #     lambda x: most_similar(x, dsa["PRESIDENTE"].to_list(), fuzz.token_sort_ratio, threshold=70)
    # )
    
    # merged_df = dsa.merge(
    #     dsc, 
    #     how="left", 
    #     left_on=["CODICE U-GOV", "PRESIDENTE"], 
    #     right_on=["Cod. Corso di Studio", "Match presidente"]
    # )

    # merged_df = dsa.merge(dsc, how="left", left_on="PRESIDENTE", right_on="Match presidente")
    
    dataset_manager = DatasetManager()
    dataset_manager.scrivi_presidenti(merged_df, "presidenti")
    
    
    
    # Carica i file strutturalmente identici e li combina in un unico DataFrame
    immatricolati_dfs = []
    for path in paths_immatricolati:
        immatricolati_dfs.append(pd.read_excel(path, engine="openpyxl", dtype=str))

    # Combina tutti i DataFrame caricati in uno unico
    immatricolati_df = pd.concat(immatricolati_dfs, ignore_index=True)
    immatricolati_df = immatricolati_df[["Codice CdL", "Valore Indicatore"]]
    immatricolati_df = immatricolati_df.rename(columns={"Codice CdL" : "Cod. Corso di Studio"})
    
    immatricolati_df["Valore Indicatore"] = immatricolati_df["Valore Indicatore"].astype(int)
    
    data = data.merge(
        immatricolati_df,
        on="Cod. Corso di Studio",
        how="left"
    )
    data = data.rename(columns={"Valore Indicatore": "Immatricolati"})
    
    # carica il df al path di "path_elenco_allegato" e mappa su "Massimo Teorico" del df "data"
    # i valori contenuti nella colonna "N. max" dove il "Cod. Corso di Studio" (data) è uguale a "CODICE U-GOV"(df_allegato)
    df_allegato = pd.read_excel(path_elenco_allegato, engine="openpyxl", dtype=str)
    mapping_massimo_teorico = df_allegato.set_index("CODICE U-GOV")["N. max"].to_dict()
    data["Massimo Teorico"] = data["Cod. Corso di Studio"].map(mapping_massimo_teorico)
    # se il valore di "Massimo Teorico" è nullo, allora sostituisci con il valore di "Immatricolati"
    data["Massimo Teorico"] = data["Massimo Teorico"].fillna(data["Immatricolati"])

    # data.to_excel("tmp.xlsx", index=False)
    
    dataset_manager = DatasetManager()
    dataset_manager.scrivi_ministeriali(data, "minesteriali")

if __name__ == "__main__":
    main()