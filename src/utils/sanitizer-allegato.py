import pandas as pd
import openpyxl

file_path = "../dataset/allegato-d.ods"

# Carica i due fogli
sheet1_df = pd.read_excel(file_path, engine="odf", sheet_name=0, dtype=str)
sheet2_df = pd.read_excel(file_path, engine="odf", sheet_name=1, dtype=str)

# Rimuovi gli spazi prima e dopo nelle colonne di interesse e convertili in minuscolo
sheet1_df["Area"] = sheet1_df["Area"].str.strip().str.lower()
sheet1_df["Codice area"] = sheet1_df["Codice area"].str.strip().str.lower()

sheet2_df["Area"] = sheet2_df["Area"].str.strip().str.lower()
sheet2_df["Codice area"] = sheet2_df["Codice area"].str.strip().str.lower()

# Esegui il merge tra i due DataFrame
df = sheet2_df.merge(
    sheet1_df,
    left_on=["Area", "Codice area", "Tipo laurea"],
    right_on=["Area", "Codice area", "Tipo laurea"],
    how="left"
)

# Salva il risultato in un nuovo file Excel
df.to_excel("../dataset/allegato-d-sanitized.xlsx", engine="openpyxl", index=False)