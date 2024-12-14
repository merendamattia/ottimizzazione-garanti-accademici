import pandas as pd
import os
from modules.dataset_manager import DatasetManager
from modules.course_parser import CourseParser
from modules.dataset_loader import DatasetLoader
import subprocess

dataset_corsi_dir = 'dataset/corsi/'
filepathCorsi = dataset_corsi_dir + 'codici-corsi.csv'
filepathProf = dataset_corsi_dir + 'codici-matricole.csv'

path_coperture = "dataset/coperture.xlsx"
path_docenti = "dataset/docenti.xlsx"
path_docenti_a_contratto = "dataset/docenti_a_contratto.xlsx"
paths_immatricolati = ["dataset/immatricolati/LT.xlsx", "dataset/immatricolati/LM.xlsx", "dataset/immatricolati/CU.xlsx"]



def write(filters_corsi):

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


def init_matricole(filename):
    dsl = DatasetLoader(path_docenti)
    
    # Prende le matricole dei docenti non a contratto rimuovendo possibili duplicati
    matricole = dsl.get_values(columns=["Matricola"]).drop_duplicates()["Matricola"].tolist()
    
    dsl = DatasetLoader(path_coperture)
    ds = dsl.get_values(columns=["Cod. Corso di Studio", "Matricola"])
    
    # Filra gli insegnamenti per le matricole dei prof
    ds_min = dsl.filter_by_values(dataset=ds, filters={"Matricola" : matricole})
    
    dsl.save_to_file(ds_min, filename)
    
def init_corsi(filename):
    dsl = DatasetLoader(path_coperture)
    
    df = dsl.get_values(columns=["Cod. Corso di Studio", "Des. Corso di Studio", "Cod. Tipo Corso"])
    
    df["Overview"] = df["Des. Corso di Studio"].astype(str).str.lower() + "(" + df["Cod. Tipo Corso"] + ")"
    
    df = dsl.get_values(dataset=df, columns=["Cod. Corso di Studio", "Overview"])
    
    # Estrae i codici rimuovendo i duplicati
    codici_corsi = dsl.get_values(dataset=df, columns=["Cod. Corso di Studio"]).drop_duplicates()
    
    ds_min = dsl.filter_by_values(dataset=df, filters={"Cod. Corso di Studio" : codici_corsi["Cod. Corso di Studio"].tolist()})
    dsl.save_to_file(ds_min, filename)

def init_corsi_matricole(filepathCorsi, filepathProf):
    init_corsi(filepathCorsi)
    init_matricole(filepathProf)
    print("Estrazione completata. Rieseguire il programma.")
    exit()

def run():
    print("Running program...")
    output_file = "output.txt"
    ret = 0
    
    with subprocess.Popen(
        ["bash", "execute.sh"], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
    ) as process, open(output_file, "a") as f:
        # Legge l'output riga per riga
        for line in process.stdout:
            print(line.strip())
            f.write(line.strip() + "\n")

        # Attende la terminazione del processo
        process.wait()
        
    # process = subprocess.Popen(["bash", "execute.sh"], stdout=subprocess.PIPE)
    
    # for line in process.stdout:
    #     print(line.decode().strip())
    #     with open(output_file, "a") as f:
    #         f.write(line.decode().strip() + "\n")
            
    # process.wait()
    
    with open(output_file, "r") as f:
        content = f.read()
        if "UNSATISFIABLE" in content:
            ret = -1
        elif "OPTIMUM FOUND" in content:
            ret = 1
        
    # Rimuove il file temporaneo
    if os.path.exists(output_file):
        os.remove(output_file)
    
    return ret


def main():
    
    
    if not os.path.exists(dataset_corsi_dir):
        os.makedirs(dataset_corsi_dir)
    if not os.path.exists(filepathCorsi) or not os.path.exists(filepathProf):
        init_corsi_matricole(filepathCorsi, filepathProf)
    
    
    # Inizializza il Dataset Manager
    dataset_manager = DatasetManager(dataset_path=filepathCorsi)

    # Ottiene la lista dei dipartimenti
    courses = dataset_manager.get_courses()

    parser = CourseParser()
    parser.add_courses(courses)
    args = parser.parse()
    
    # print(courses)
    
    filters_corsi = {"Cod. Corso di Studio" : list()}
    if not any(vars(args).values()):
        print("Errore: nessun dipartimento selezionato.")
        parser.parser.print_help()
        exit()
        
    if args.all:
        for key in courses.keys():
            filters_corsi["Cod. Corso di Studio"].append(key)
    else:
        for key in courses.keys():
            if getattr(args, key, False):
                filters_corsi["Cod. Corso di Studio"].append(key)

    filters_corsi ["Cod. Corso di Studio"] = list(set(filters_corsi ["Cod. Corso di Studio"]))
    
    NUMERO_MINIMO_DI_INSEGNAMENTI = 9
    
    dsl = DatasetLoader(path_coperture)
    df_tmp = dsl.filter_by_values(filters=filters_corsi, only_prefix=False)
    
    # Raggruppa per codice corso e conta le occorrenze
    conteggi = df_tmp['Cod. Corso di Studio'].value_counts()

    # Filtra il DataFrame mantenendo solo i codici corso con almeno 9 occorrenze
    codici_non_validi = conteggi[conteggi <= NUMERO_MINIMO_DI_INSEGNAMENTI].index
    df_tmp = df_tmp[df_tmp['Cod. Corso di Studio'].isin(codici_non_validi)]
    
    excluded = set(df_tmp["Cod. Corso di Studio"].unique())
    #print(excluded)
    #print(filters_corsi)
    
    filters_corsi ["Cod. Corso di Studio"] = list(set(filters_corsi ["Cod. Corso di Studio"]) - excluded)
    #print(filters_corsi)

    
    
    all_codes = filters_corsi["Cod. Corso di Studio"]
    
    
    print(f"Testing one-by-one")
    banned_codes = list()
    
    for code in all_codes:
        print(f"Testing {code}")
        current_codes = {"Cod. Corso di Studio": [code]}
        write(current_codes)
        
        res = run()
        if res == -1:
            print(f"Errore con {code}")
            banned_codes.append(code)
        
    
    # scrive la lista di codici da escludere in un file (one-by-one.txt)
    banned_codes_file = "one-by-one-banned.txt"
    if len(banned_codes) > 0:
        with open(banned_codes_file, "w") as f:
            for code in banned_codes:
                f.write(f"{code}\n")
    else:
        print("No banned codes")
    
    print()
    print(f"Testing increasing tuples")
    
    # rimuove i codici bannati dalla lista dei codici utilizzati
    accepted_codes = list(set(all_codes) - set(banned_codes))
    
    current_codes = dict()
    current_codes["Cod. Corso di Studio"] = list()
    banned_codes = list()
    accepted_lines = list()
    
    for code in accepted_codes:
        current_codes["Cod. Corso di Studio"].append(code)
        
        print(f"Testing {current_codes['Cod. Corso di Studio']}")
        
        write(current_codes)
        
        res = run()
        if res == -1:
            print(f"Errore con {code}")
            banned_codes.append(f"{code}, {current_codes["Cod. Corso di Studio"]}")
            current_codes["Cod. Corso di Studio"].pop()
        elif res == 1:
            print("OPTIMUM FOUND")
            accepted_lines.append(f"OPTIMUM FOUND, {current_codes["Cod. Corso di Studio"]}")
        elif res == 0:
            print("SATISFABLE")
            accepted_lines.append(f"SATISFABLE, {current_codes["Cod. Corso di Studio"]}")
    
    if len(banned_codes) > 0:
        with open("increasing-banned.txt", "a") as f:
            for line in banned_codes:
                f.write(f"{line}\n")
    else:
        print("No banned tuples")
    
    if len(accepted_lines) > 0:
        with open("increasing-accepted.txt", "a") as f:
            for line in accepted_lines:
                f.write(f"{line}\n")
    else:
        print("No accepted lines")



if __name__ == "__main__":
    main()