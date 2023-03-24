class Menuview:

    @staticmethod
    def welcome():
        print(f'Bienvenue dans ce logiciel de tournoi d’échecs')

    @staticmethod
    def askcommandmenu():
        print(f'Ou voulez-vous aller? Tournoi | Joueur | Exit')
        return input()

    @staticmethod
    def goodbye():
        print(f'Au revoir! Merci d\'avoir utiliser ce logiciel')
