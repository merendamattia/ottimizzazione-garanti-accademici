from argparse import ArgumentParser

class CourseParser:
    def __init__(self):
        """
        Inizializza il parser per i corsi.
        """
        self.parser = ArgumentParser(description="Seleziona il corso da caricare")
        self.parser.add_argument("--all", action="store_true", help="Seleziona tutti i corsi")

    def add_courses(self, courses):
        """
        Aggiunge argomenti dinamici per ciascun dipartimento.
        :param departments: Lista dei corsi.
        """
        for code, name  in courses.items():
            self.parser.add_argument(f"--{code}", action="store_true", help=f"Seleziona il corso {name} ({code})")

    def parse(self):
        """
        Effettua il parsing degli argomenti.
        :return: Gli argomenti parsati.
        """
        return self.parser.parse_args()