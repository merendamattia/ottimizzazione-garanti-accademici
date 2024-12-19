from argparse import ArgumentParser

class CourseParser:
    """
    Classe gestire il parsing dei corsi utilizzando il modulo argparse.
    Consente di aggiungere corsi come argomenti dinamici e di effettuare il parsing
    degli argomenti della riga di comando.
    """
    def __init__(self):
        """
        Inizializza il parser per i corsi.
        Il parser supporta l'argomento `--all` per selezionare tutti i corsi.
        """
        self.parser = ArgumentParser(description="Seleziona il corso da caricare")
        self.parser.add_argument("--all", action="store_true", help="Seleziona tutti i corsi")

    def add_courses(self, courses):
        """
        Ogni corso viene aggiunto come un argomento con nome `--<codice>`, 
        dove `<codice>` rappresenta il codice del corso.

        :param courses: Dizionario contenente i corsi. La chiave è il codice del corso 
                        (str), mentre il valore è il nome del corso (str).
        :type courses: dict
        """
        for code, name  in courses.items():
            self.parser.add_argument(f"--{code}", action="store_true", help=f"Seleziona il corso {name} ({code})")

    def parse(self):
        """
        Effettua il parsing degli argomenti della riga di comando.

        :return: Un oggetto contenente gli argomenti parsati come attributi.
        :rtype: argparse.Namespace
        """
        return self.parser.parse_args()