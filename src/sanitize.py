# %%
import pandas as pd
import openpyxl

path_ns_coperture = "dataset/coperture.xlsx"
path_ns_docenti = "dataset/docenti.xlsx"

path_coperture = "dataset/coperture_sanitized.xlsx"
path_docenti = "dataset/docenti_sanitized.xlsx"

# %%
def sanitize_docenti():
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
    df = pd.read_excel(path_ns_coperture, engine="openpyxl", dtype=str)
    print(df)
    # Rimuovere le righe che hanno il campo matricola vuoto
    df = df.dropna(subset=["Matricola"])
    print(df)
    df["Matricola"] = df["Matricola"].astype(int)
    print(df)
    df["Matricola"] = df["Matricola"].astype(str)
    # astype
    matricole = pd.read_excel(path_docenti, engine="openpyxl", dtype=str)["Matricola"]
    print(matricole)
    df = df[df["Matricola"].isin(matricole)]
    
    df.to_excel(path_coperture, index=False)
# %%
def sanitize():
    sanitize_docenti()
    sanitize_coperture()

# %%
if __name__ == "__main__":
    sanitize()
# %%
