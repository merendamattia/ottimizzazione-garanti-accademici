from modules.dataset_manager import DatasetManager
from modules.department_parser import DepartmentParser
from modules.dataset_loader import DatasetLoader
from tqdm import tqdm
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from collections import defaultdict
import shutil

###################################### TEST ######################################

def test_parser():
    # Inizializza il Dataset Manager
    dataset_manager = DatasetManager(dataset_path="dataset/ssd/")

    # Ottiene la lista dei dipartimenti
    departments = dataset_manager.get_departments()
    if not departments:
        print("Errore: nessun file trovato nella cartella dataset.")
        return

    # Crea un'istanza del parser e ottiene gli argomenti
    parser = DepartmentParser()
    parser.add_departments(departments)
    args = parser.parse()

    print(departments)

    # Logica per gestire i dipartimenti selezionati
    if args.all:
        print("Caricamento dati per tutti i dipartimenti...")
        for dep in departments:
            dataset_manager.load_data(dep)
    else:
        for dep in departments:
            if getattr(args, dep, False):
                # Qui devo andare ad estrapolare i dati per ogni scelta
                dataset_manager.load_data(dep)

    # Se nessun argomento è specificato
    if not any(vars(args).values()):
        print("Errore: nessun dipartimento selezionato.")
        parser.parser.print_help()

def test_filtra_per_valori():
    dataset_loader = DatasetLoader('dataset/coperture.xlsx')

    filters = {
        'Cod. Tipo Corso': ['LM'],
        'SSD': ['INF/01']
    }
    filtered_data = dataset_loader.filter_by_values(filters)

    dataset_loader.save_to_file(df=filtered_data, output_file_path='dataset/tmp_info.csv')

def test_filtra_per_colonne():
    dataset_loader = DatasetLoader('dataset/coperture.xlsx')

    filters = {
        'Cod. Tipo Corso': ['LM'],
        'SSD': ['INF/01']
    }
    data = dataset_loader.filter_by_values(filters=filters)

    columns = [
        'Cognome',
        'Matricola',
        'Cod. Att. Form.', # ID insegnamento
        'Des. Insegnamento',
        'CFU'
    ]
    data = dataset_loader.get_values(dataset=data, columns=columns)
    print(data)

def test_estrazione_settori():
    dsl = DatasetLoader('dataset/coperture.xlsx')
    filters = ['SSD']
    ds = dsl.get_values(columns=filters)
    
    SSD = dsl.df_to_dict(ds)

    dsm = DatasetManager()
    settori = dsm.get_sectors(SSD['SSD'])
    print(settori)

def run_tests():
    test_filtra_per_valori()
    test_filtra_per_colonne()
    scrittura_fatti()
    test_estrazione_settori()
    estrazione_dati_per_ssd()
    test_parser()

###################################### FUNZIONI PRINCIPALI ######################################

def scrittura_fatti(filters=None, file_name=None, path='dataset/coperture.xlsx'):
    """
    Filtra i dati da un dataset Excel basandosi sui criteri forniti e scrive i fatti in un file ASP.

    :param filters: Dizionario contenente i criteri di filtraggio.
                    Esempio:
                    {
                        'Cod. Tipo Corso': ['LM'],
                        'SSD': ['INF/01']
                    }
                    Se non specificato, vengono utilizzati i valori predefiniti: 
                    {'Cod. Tipo Corso': ['LM'], 'SSD': ['INF/01']}.
    :param file_name: Nome del file di output (senza estensione) dove verranno salvati i fatti generati.
                      Se non specificato, il file verrà salvato con il nome predefinito "test".

    Funzionamento:
    1. Inizializza un'istanza di `DatasetLoader` per caricare i dati dal file `dataset/coperture.xlsx`.
    2. Filtra i dati in base ai criteri specificati in `filters`.
    3. Inizializza un'istanza di `DatasetManager`.
    4. Utilizza il metodo `write_atoms` del `DatasetManager` per scrivere i fatti filtrati nel file ASP specificato.

    Esempio:
    --------
    Se il dataset contiene corsi con SSD 'INF/01' e tipo corso 'LM', e il filtro fornito è:
    filters = {
        'Cod. Tipo Corso': ['LM'],
        'SSD': ['INF/01']
    }
    e `file_name = "informatica"`, i dati filtrati verranno salvati nel file `informatica.lp`.

    :raises FileNotFoundError: Se il file specificato nel DatasetLoader non esiste.
    :raises Exception: Per altri errori durante il filtraggio o la scrittura dei fatti.
    """
    if filters is None:
        filters = {
            'Cod. Tipo Corso': ['LM'],
            'SSD': ['INF/01']
        }
    if file_name is None:
        file_name = 'test'
    
    dataset_loader = DatasetLoader(path)
    data = dataset_loader.filter_by_values(filters=filters)
    dataset_manager = DatasetManager()
    dataset_manager.write_atoms(data, file_name)

def process_ssd(dataset_loader, ssd, failed_ssds):
    """
    Elabora un singolo valore SSD, applicando il filtro e salvando il file.
    :param dataset_loader: Istanza di DatasetLoader.
    :param ssd: Valore dell'SSD da elaborare.
    :param failed_ssds: Set per raccogliere gli SSD che causano errori.
    """
    try:
        filters = {
            'SSD': [f'{ssd}']
        }
        filtered_data = dataset_loader.filter_by_values(filters)

        # Converte in minuscolo e sostituisce '/' con '_'
        ssd_name = str(ssd).lower().replace('/', '_')

        # Salva il file
        dataset_loader.save_to_file(df=filtered_data, output_file_path=f'dataset/ssd/{ssd_name}.csv')
    except Exception as e:
        # Aggiunge l'SSD al set dei falliti e stampa l'errore
        failed_ssds.add(str(ssd))  # Converte in stringa per evitare errori di tipo
        print(f"Errore durante l'elaborazione dell'SSD {ssd}: {e}")

def estrazione_dati_per_ssd(path='dataset/coperture.xlsx'):
    """
    Estrae i dati per ogni SSD, applicando il filtro e salvando i file CSV nella cartella 'dataset/ssd/'.

    Questa funzione esegue le seguenti operazioni:
    1. Carica i dati da un file Excel e seleziona la colonna 'SSD', rimuovendo i duplicati.
    2. Crea una barra di progresso per monitorare l'elaborazione degli SSD.
    3. Utilizza un `ThreadPoolExecutor` per elaborare i dati in parallelo, migliorando le performance.
    4. Crea la cartella di output 'dataset/ssd/' se non esiste già.
    5. Per ogni SSD, chiama la funzione `process_ssd` per applicare il filtro e salvare il file CSV corrispondente.
    6. Gestisce gli errori durante l'elaborazione e registra gli SSD che non sono stati salvati.

    :param dataset_loader: Istanza di `DatasetLoader` per accedere ai metodi di filtraggio e salvataggio.
    :param failed_ssds: Set per raccogliere gli SSD che causano errori durante l'elaborazione.
    """
    
    dataset_loader = DatasetLoader(path)
    columns = ['SSD']
    data = dataset_loader.get_values(columns=columns).drop_duplicates()
    # print(data)

    total_rows = len(data)
    failed_ssds = set()  # Set per raccogliere gli SSD che non sono stati salvati

    # Crea la cartella 'dataset/ssd/' se non esiste
    output_dir = 'dataset/ssd/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Barra di progresso
    with tqdm(total=total_rows, desc="Elaborazione SSD...") as pbar:
        # Us0 ThreadPoolExecutor per parallelizzare l'elaborazione
        with ThreadPoolExecutor(max_workers=6) as executor:  # Imposta il numero di thread desiderato
            future_to_ssd = {executor.submit(process_ssd, dataset_loader, row['SSD'], failed_ssds): row['SSD'] for _, row in data.iterrows()}

            for future in as_completed(future_to_ssd):
                pbar.update(1)

    # Stampa quali SSD non sono stati salvati
    if failed_ssds:
        print(f"Gli SSD non salvati a causa di errori sono: {', '.join(failed_ssds)}")

def unisci_file_per_settore(path):
    """
    Unisce i file CSV che hanno lo stesso settore in base al prefisso del nome file.
    Salva il risultato in un unico file per settore senza duplicare l'intestazione.
    Sposta i file originali con '_' nel nome nella cartella 'caratterizzanti'.
    
    :param path: Percorso alla cartella contenente i file CSV.
    """
    # Dizionario per raccogliere i DataFrame per ogni settore
    file_per_settore = defaultdict(list)
    caratterizzanti_path = os.path.join(path, "caratterizzanti")

    # Crea la cartella "caratterizzanti" se non esiste
    if not os.path.exists(caratterizzanti_path):
        os.makedirs(caratterizzanti_path)

    # Controlla se la cartella principale esiste
    if not os.path.exists(path):
        print(f"Errore: La cartella '{path}' non esiste.")
        return

    # Itera su tutti i file nella cartella
    for filename in os.listdir(path):
        if filename.endswith('.csv') and '_' in filename:
            # Ottiene il settore dal nome del file (parte prima del '_')
            settore = filename.split('_')[0]
            full_path = os.path.join(path, filename)

            try:
                # Carica il file CSV e lo aggiunge al settore corrispondente
                df = pd.read_csv(full_path)
                file_per_settore[settore].append(df)
            except Exception as e:
                print(f"Errore durante la lettura del file '{filename}': {e}")

    # Unisce i DataFrame per ogni settore e salva il risultato
    for settore, dfs in file_per_settore.items():
        try:
            # Unisce i DataFrame per il settore senza duplicare l'intestazione
            output_file = os.path.join(path, f"{settore}.csv")
            
            # Scrive il primo file con l'intestazione
            dfs[0].to_csv(output_file, index=False, mode='w', header=True)
            
            # Scrive i file successivi senza intestazione
            for df in dfs[1:]:
                df.to_csv(output_file, index=False, mode='a', header=False)
            
            print(f"File unito salvato per settore '{settore}': {output_file}")
        except Exception as e:
            print(f"Errore durante la scrittura del file per il settore '{settore}': {e}")

    # Sposta i file originali nella cartella 'caratterizzanti'
    for filename in os.listdir(path):
        if filename.endswith('.csv') and '_' in filename:
            source_path = os.path.join(path, filename)
            destination_path = os.path.join(caratterizzanti_path, filename)
            try:
                shutil.move(source_path, destination_path)
                print(f"File spostato: {filename} -> {destination_path}")
            except Exception as e:
                print(f"Errore durante lo spostamento del file '{filename}': {e}")

def init():
    print("Errore: nessun file trovato nella cartella dataset.")
    print("Estrazione file in corso...")
    estrazione_dati_per_ssd(path='dataset/docenti.xlsx')
    unisci_file_per_settore(path='dataset/ssd')
    print("Estrazione completata. Rieseguire il programma.")
    exit()

if __name__ == "__main__":
    
    # Se la cartella non esiste, lancio la generazione dei dataset
    dataset_dir = 'dataset/ssd/'
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)
        init()

    # Inizializza il Dataset Manager
    dataset_manager = DatasetManager(dataset_path=dataset_dir)

    # Ottiene la lista dei dipartimenti
    departments = dataset_manager.get_departments()

    # Se la cartella esiste ma è vuota, lancio la generazione dei dataset
    if not departments:
        init()

    # Crea un'istanza del parser e ottiene gli argomenti
    parser = DepartmentParser()
    parser.add_departments(departments)
    args = parser.parse()

    # Filtro SSD costruito dinamicamente
    filters = {'SSD': []}

    def add_to_filter(dep):
        """
        Aggiunge i valori trasformati di `dep` al filtro SSD.
        :param dep: Stringa contenente SSD separati da virgola (es. 'l-fil-let_13, vet_05').
        """
        # Divide i valori separati da virgola, rimuove spazi e trasforma
        transformed_ssds = [s.strip().upper().replace('_', '/') for s in dep.split(',')]
        filters['SSD'].extend(transformed_ssds)

    # Logica per gestire i dipartimenti selezionati
    if args.all:
        print("Caricamento dati per tutti i dipartimenti...")
        for dep in departments:
            add_to_filter(dep)  
    else:
        for dep in departments:
            if getattr(args, dep, False):
                add_to_filter(dep)  

    # Rimuove eventuali duplicati dal filtro SSD
    filters['SSD'] = list(set(filters['SSD']))

    # Se nessun argomento è specificato
    if not any(vars(args).values()):
        print("Errore: nessun dipartimento selezionato.")
        parser.parser.print_help()
        exit()

    ### SCRITTURA DOCENTI 
    dataset_loader = DatasetLoader('dataset/docenti_sanitized.xlsx')
    data = dataset_loader.filter_by_values(filters=filters, only_prefix=True)
    dataset_manager = DatasetManager()
    dataset_manager.scrivi_docenti(data, 'docenti')

    ### SCRITTURA CORSI
    dataset_loader = DatasetLoader('dataset/coperture_sanitized.xlsx')
    data = dataset_loader.filter_by_values(filters=filters, only_prefix=True)
    dataset_manager = DatasetManager()
    dataset_manager.scrivi_coperture(data, 'coperture')