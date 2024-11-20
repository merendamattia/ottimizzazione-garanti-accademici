from argparse import ArgumentParser

class DepartmentParser:
    def __init__(self):
        """
        Inizializza il parser per i dipartimenti.
        """
        self.parser = ArgumentParser(description="Seleziona i dipartimenti da caricare")
        self.parser.add_argument("--all", action="store_true", help="Seleziona tutti i dipartimenti")

    def add_departments(self, departments):
        """
        Aggiunge argomenti dinamici per ciascun dipartimento.
        :param departments: Lista dei dipartimenti.
        """
        for dep in departments:
            self.parser.add_argument(f"--{dep}", action="store_true", help=f"Seleziona il dipartimento {dep}")

    def parse(self):
        """
        Effettua il parsing degli argomenti.
        :return: Gli argomenti parsati.
        """
        return self.parser.parse_args()