from docx import Document
import pandas as pd
import re

file_path = "../dataset/originali/elenco_2024-2025.docx" 
doc = Document(file_path)

tabelle = []

for table in doc.tables:
    tabella = []
    for row in table.rows:
        row = [cell.text.strip() for cell in row.cells]
        tabella.append(row)
    tabelle.append(tabella)

rows = []

for i, tabella in enumerate(tabelle):
    print(f"Tabella {i+1}:")
    dipartimento = ""

    for row in tabella:
        if any(re.search(r"\bDIPARTIMENTO\b", cell, re.IGNORECASE) for cell in row):
            dipartimento = " ".join(row).replace("DIPARTIMENTO", "").strip()
            dipartimento = "DIPARTIMENTO" + dipartimento 
            continue 
        
        if any(re.search(r"\bCODICE U-GOV\b", cell, re.IGNORECASE) for cell in row):
            continue

        all_empty = True
        for cell in row:
            if cell.strip():
                all_empty = False
                break
        if all_empty:
            continue
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

df = pd.DataFrame(rows, columns=["CORSO DI STUDIO","CORSO DI STUDIO", "CODICE U-GOV", "CLASSE", "PRESIDENTE", "NOTE", "DOCENZA DI RIFERIMENTO", "DIPARTIMENTO"])
df = df.loc[:, ~df.columns.duplicated()]
df.to_excel("dataset/elenco_2024-2025.xlsx", index=False)
print("File Excel salvato con successo!")
