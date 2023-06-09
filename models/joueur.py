class Joueur:
    """A player"""
    def __init__(self, ine, lastname: str, name: str, birthdate: str):
        self.lastname = lastname
        self.name = name
        self.birthdate = birthdate
        self.ine = ine

    def todict(self):
        my_dict = {'ine': self.ine,
                   'lastname': self.lastname,
                   'name': self.name,
                   'birthdate': self.birthdate,
                   }
        return my_dict
