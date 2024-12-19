import re
from collections import defaultdict
import argparse
import pandas as pd
import json

DEV = False
# Parsing arguments
parser = argparse.ArgumentParser(description="Estrai l'ultima risposta da un file Clingo e genera una struttura dati.")
parser.add_argument("filepath", type=str, help="Percorso del file da analizzare.")
args = parser.parse_args()

garanti = defaultdict(list)

try:
    with open(args.filepath, "r") as file:
        content = file.read()
except FileNotFoundError:
    print(f"Errore: Il file '{args.filepath}' non esiste.")
    exit(1)

print("Loading file...")
answerBlocks = re.findall(r"(Answer: \d+\n.*?Optimization: -?\d+)", content, re.DOTALL)

print("Processing...")
if answerBlocks:
    last_block = answerBlocks[-1]
    matches = re.findall(r"garante\((\d+),(\d+),\d+,(\w+)\)", last_block)

    for matricola_docente, codice_corso, quarto_elemento in matches:
        if (matricola_docente, codice_corso, quarto_elemento) not in garanti[codice_corso]:
            garanti[codice_corso].append((matricola_docente, quarto_elemento))


path_coperture = "../dataset/coperture.xlsx"
path_docenti = "../dataset/docenti.xlsx"



df_docenti = pd.read_excel(path_docenti, engine="openpyxl", dtype=str)
df_docenti = df_docenti[["Matricola", "Cognome e Nome"]]
df_docenti["Matricola"] = df_docenti["Matricola"].astype(int)
df_docenti["Matricola"] = df_docenti["Matricola"].astype(str)

df_coperture = pd.read_excel(path_coperture, engine="openpyxl", dtype=str)
df_coperture = df_coperture[["Cod. Corso di Studio", "Des. Corso di Studio"]]
df_coperture["Cod. Corso di Studio"] = df_coperture["Cod. Corso di Studio"].astype(int)
df_coperture["Cod. Corso di Studio"] = df_coperture["Cod. Corso di Studio"].astype(str)

result = []
jolly_data = []

for codice_corso, docenti in garanti.items():
    nome_corso = df_coperture.loc[
        df_coperture["Cod. Corso di Studio"] == codice_corso, 
        "Des. Corso di Studio"
    ].values
    
    
    matricole = [int(docente[0]) for docente in docenti if docente[1] != "c"]
    nome_docenti = df_docenti.loc[
        df_docenti["Matricola"].isin(map(str, matricole)), 
        "Cognome e Nome"
    ].tolist()
    
    num_jolly = len(docenti) - len(matricole)
    
    result.append({
        "Codice corso": codice_corso,
        "Matricole": matricole,
        "Nome docenti": nome_docenti,
        "Nome corso": nome_corso[0] if len(nome_corso) > 0 else "Non trovato",
        "Jolly": "No" if num_jolly == 0 else "Si"
    })
    
    jolly_data.append({
        "Codice Corso": codice_corso,
        "Des. Corso": nome_corso[0] if len(nome_corso) > 0 else "Non trovato",
        "Numero di Jolly": num_jolly
    })


if DEV:
    output_path = "result.json"
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)
    print(f"JSON salvato in '{output_path}'.")


print("Salvataggio in Excel...")
excel_data = []


for entry in result:
    codice_corso = entry["Codice corso"]
    nome_corso = entry["Nome corso"]
    for matricola, nome_docente in zip(entry["Matricole"], entry["Nome docenti"]):
        excel_data.append({
            "Cognome e Nome": nome_docente,
            "Matricole": str(matricola),
            "Codice Corso": str(codice_corso),
            "Des. Corso": nome_corso
        })


excel_output_path = "garanti.xlsx"
jolly_output_path = "contratti.xlsx"

df_excel = pd.DataFrame(excel_data, columns=["Cognome e Nome", "Matricole", "Codice Corso", "Des. Corso"])
df_excel["Matricole"] = df_excel["Matricole"].astype(str)
df_excel["Codice Corso"] = df_excel["Codice Corso"].astype(str)

df_excel.to_excel(excel_output_path, index=False, engine="openpyxl")
print(f"File Excel salvato in '{excel_output_path}'.")

df_jolly = pd.DataFrame(jolly_data, columns=["Codice Corso", "Des. Corso", "Numero di Jolly"])
df_jolly = df_jolly[df_jolly["Numero di Jolly"] > 0]

if not df_jolly.empty:
    df_jolly = df_jolly.rename(columns={"Numero di Jolly": "Numero di Contratti"})
    df_jolly.to_excel(jolly_output_path, index=False, engine="openpyxl")
    print(f"File Excel con i contratti salvato in '{jolly_output_path}'.")
else:
    print("Nessun corso con contratti trovato, file non creato.")