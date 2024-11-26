from modules.dataset_manager import DatasetManager
from modules.department_parser import DepartmentParser
from modules.dataset_loader import DatasetLoader

def test_parser():
    # Inizializza il Dataset Manager
    dataset_manager = DatasetManager()

    # Ottiene la lista dei dipartimenti
    departments = dataset_manager.get_departments()
    if not departments:
        print("Errore: nessun file trovato nella cartella dataset.")
        return

    # Crea un'istanza del parser e ottiene gli argomenti
    parser = DepartmentParser()
    parser.add_departments(departments)
    args = parser.parse()

    # Logica per gestire i dipartimenti selezionati
    if args.all:
        print("Caricamento dati per tutti i dipartimenti...")
        for dep in departments:
            dataset_manager.load_data(dep)
    else:
        for dep in departments:
            if getattr(args, dep, False):
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

def test_scrittura_atomi():
    dataset_loader = DatasetLoader('dataset/coperture.xlsx')

    filters = {
        # 'Cod. Tipo Corso': ['LM'],
        'SSD': ['INF/01']
    }
    data = dataset_loader.filter_by_values(filters=filters)

    dataset_manager = DatasetManager()
    dataset_manager.write_atoms(data, 'informatica')


def test_estrazione_settori():
    dsl = DatasetLoader("dataset/coperture.xlsx")
    filters = ["SSD"]
    ds = dsl.get_values(columns=filters)
    
    SSD = dsl.df_to_dict(ds)
    # print(SSD)
    # print(SSD.keys())
    dsm = DatasetManager()
    settori = dsm.get_sectors(SSD["SSD"])
    print(settori)


if __name__ == "__main__":
    # test_parser()
    # test_filtra_per_valori()
    # test_filtra_per_colonne()
    # test_scrittura_atomi()
    test_estrazione_settori()