from modules.loader import Loader
from modules.department_parser import DepartmentParser

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

if __name__ == "__main__":
    main()