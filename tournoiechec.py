import os
from controllers.menumanager import MenuManager


def make_a_dir(name):
    """Création des dossiers pour récupérer les data json"""
    try:
        os.mkdir(name)
    except FileExistsError:
        pass


# Initialize data from files
make_a_dir('./data/')
make_a_dir('./data/tournaments/')

# Launch the program
new_tmanager = MenuManager()
