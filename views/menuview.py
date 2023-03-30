class Menuview:

    @staticmethod
    def welcome():
        print('Bienvenue dans ce logiciel de tournoi d’échecs')

    @staticmethod
    def askcommandmenu():
        print('Ou voulez-vous aller? Tournoi | Joueur | Exit')
        return input()

    @staticmethod
    def goodbye():
        print('Au revoir! Merci d\'avoir utiliser ce logiciel')
