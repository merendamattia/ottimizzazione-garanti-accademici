import pandas as pd
import openpyxl

file_path = "../dataset/allegato-d.ods"

sheet1_df = pd.read_excel(file_path, engine="odf", sheet_name=0, dtype=str)
sheet2_df = pd.read_excel(file_path, engine="odf", sheet_name=1, dtype=str)
# print("Contenuto del primo foglio:")
# print(sheet1_df)

# print("\nContenuto del secondo foglio:")
# print(sheet2_df)

sheet1_df["Area"] = sheet1_df["Area"].str.strip().str.lower()
sheet1_df["Codice area"] = sheet1_df["Codice area"].str.strip().str.lower()

sheet2_df["Area"] = sheet2_df["Area"].str.strip().str.lower()
sheet2_df["Codice area"] = sheet2_df["Codice area"].str.strip().str.lower()

df = sheet2_df.merge(
    sheet1_df,
    left_on=["Area", "Codice area", "Tipo laurea"],
    right_on=["Area", "Codice area", "Tipo laurea"],
    how="left"
)

df.to_excel("../dataset/allegato-d-sanitized.xlsx", engine="openpyxl", index=False)