from modules.dataset_manager import DatasetManager
from modules.course_parser import CourseParser
from modules.dataset_loader import DatasetLoader
import os
import pandas as pd


############################## VARIABILI GLOBALI #################################

# Percorso del file contenente i dati sulle coperture
path_coperture = "dataset/coperture.xlsx"

# Percorso del file contenente i dati dei docenti
path_docenti = "dataset/docenti.xlsx"

# Percorso del file contenente i dati dei docenti a contratto
path_docenti_a_contratto = "dataset/docenti_a_contratto.xlsx"

# Elenco dei file contenenti i dati degli immatricolati (LT, LM, CU)
paths_immatricolati = ["dataset/immatricolati/LT.xlsx", "dataset/immatricolati/LM.xlsx", "dataset/immatricolati/CU.xlsx"]

# Numero minimo di insegnamenti richiesti per considerare valido un corso
NUMERO_MINIMO_DI_INSEGNAMENTI = 9

###################################### FUNZIONI PRINCIPALI ######################################

def init_matricole(filename):
    """
    Carica e salva le matricole dei docenti non a contratto.
    
    Args:
        filename (str): Nome del file di output.
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
    
    Args:
        filename (str): Nome del file di output.
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
    
    Args:
        filepathCorsi (str): Percorso del file di output per i corsi.
        filepathProf (str): Percorso del file di output per le matricole.
    """
    init_corsi(filepathCorsi)
    init_matricole(filepathProf)
    print("Estrazione completata. Rieseguire il programma.")
    exit()

def main():
    """
    Funzione principale per l'elaborazione e la gestione dei dati.
    
    - Inizializza i dataset dei corsi e delle matricole se non esistono.
    - Filtra e salva i dati dei corsi, docenti e coperture.
    - Genera i file richiesti in base ai parametri specificati.
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
    
    # TODO Aggiornare quando si avranno i massimi teorici per ciascun corso
    # data["Massimo Teorico"] = 250
    data["Massimo Teorico"] = data["Immatricolati"]
    
    dataset_manager = DatasetManager()
    dataset_manager.scrivi_ministeriali(data, "minesteriali")

if __name__ == "__main__":
    main()