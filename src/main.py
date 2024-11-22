from modules.loader import Loader
from modules.department_parser import DepartmentParser
from modules.dataset_loader import DatasetLoader

def main():
    # Inizializza il Loader
    loader = Loader()

    # Ottiene la lista dei dipartimenti
    departments = loader.get_departments()
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
            loader.load_data(dep)
    else:
        for dep in departments:
            if getattr(args, dep, False):
                loader.load_data(dep)

    # Se nessun argomento è specificato
    if not any(vars(args).values()):
        print("Errore: nessun dipartimento selezionato.")
        parser.parser.print_help()

def test_dataset_loader():
    dataset_loader = DatasetLoader('dataset/coperture.xlsx')

    filters = {
        'Cod. Tipo Corso': ['LM'],
        'SSD': ['INF/01']
    }
    filtered_data = dataset_loader.filter_by_values(filters)

    dataset_loader.save_to_file(df=filtered_data, output_file_path='dataset/tmp_info.csv')

if __name__ == "__main__":
    # main()
    test_dataset_loader()
