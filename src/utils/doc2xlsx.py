from docx import Document
import pandas as pd
import re

file_path = "../dataset/originali/elenco_2024-2025.docx" 
doc = Document(file_path)

tabelle = []
# Estrai tutte le tabelle dal documento

for table in doc.tables:
    tabella = []
    for row in table.rows:
        row = [cell.text.strip() for cell in row.cells]
        tabella.append(row)
    tabelle.append(tabella)

# Lista per le righe da inserire nel DataFrame
rows = []

# Lista per le righe da inserire nel DataFrame
for i, tabella in enumerate(tabelle):
    print(f"Tabella {i+1}:")
    dipartimento = ""

    for row in tabella:
        # Se una cella contiene la parola "DIPARTIMENTO", aggiorna il nome del dipartimento
        if any(re.search(r"\bDIPARTIMENTO\b", cell, re.IGNORECASE) for cell in row):
            dipartimento = " ".join(row).replace("DIPARTIMENTO", "").strip()
            dipartimento = "DIPARTIMENTO" + dipartimento 
            continue 
        
        # Se una cella contiene "CODICE U-GOV", ignorala
        if any(re.search(r"\bCODICE U-GOV\b", cell, re.IGNORECASE) for cell in row):
            continue

        all_empty = True
        for cell in row:
            if cell.strip():
                all_empty = False
                break
        if all_empty:
            continue
        
        # Controlla che la riga abbia almeno 6 colonne
        if len(row) >= 6:
            rows.append({
                "CORSO DI STUDIO": row[0],
                "CORSO DI STUDIO": row[1],
                "CODICE U-GOV": row[2],
                "CLASSE": row[3],
                "PRESIDENTE": row[4],
                "NOTE": row[5],
                "DOCENZA DI RIFERIMENTO": row[6],
                "DIPARTIMENTO": dipartimento
            })
        else:
            print(f"Riga ignorata per lunghezza insufficiente: {row}")
        print(row)
    print()

# Crea il DataFrame e rimuove eventuali colonne duplicate
df = pd.DataFrame(rows, columns=["CORSO DI STUDIO","CORSO DI STUDIO", "CODICE U-GOV", "CLASSE", "PRESIDENTE", "NOTE", "DOCENZA DI RIFERIMENTO", "DIPARTIMENTO"])
df = df.loc[:, ~df.columns.duplicated()]

# Salva il DataFrame in un file Excel
df.to_excel("dataset/elenco_2024-2025.xlsx", index=False)
print("File Excel salvato con successo!")
