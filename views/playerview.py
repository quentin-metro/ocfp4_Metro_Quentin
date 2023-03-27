from controllers.playermanager import PlayerManager
from controllers.myappexception import MyAppBadPlayerINE


class PlayerView:
    def __init__(self, playermanager: PlayerManager):
        self.playermanager = playermanager

    def askcommandplayer(self):
        while True:
            print(f'\n'
                  f'Quel action souhaitez vous effectuer?\n'
                  f'Voir la liste des joueurs | Liste\n'
                  f'Ajouter un joueur | Ajouter\n'
                  f'Retour Menu | Menu')
            choice = input().casefold()
            if choice == "liste":
                self.viewplayerlist()
            elif choice == "ajouter":
                self.addplayer()
            elif choice == "menu":
                break
            else:
                print(f'Commande non comprise\n\n')

    def viewplayerlist(self):
        playerlist = self.playermanager.getplayerlistindict()
        if playerlist:
            print(f'\n'
                  f'   INE  | Date de Naissance | Nom Prenom')
            for player in playerlist:
                ine = player['ine']
                lastname = player['lastname']
                name = player['name']
                birthdate = player['birthdate']
                print(f'{ine} |     {birthdate}      | {lastname} {name}')
        else:
            print(f'\n Aucun joueur connu\n')

    def addplayer(self):
        player_ine = input('INE: ')
        # Check if player_ine is in the correct format AB12345
        try:
            self.playermanager.ineformat(player_ine)
        except MyAppBadPlayerINE as e:
            print(e)
        else:
            # Check if player_ine exist already in data and display the info
            player_ine = player_ine.upper()
            player = self.playermanager.getplayerinfo(player_ine)
            if player:
                ine = player['ine']
                lastname = player['lastname']
                name = player['name']
                birthdate = player['birthdate']
                print(f'{player_ine} existe déjà\n'
                      f'{ine} |     {birthdate}      | {lastname} {name}')
                return
            lastname = input('Nom: ')
            name = input('Prenom: ')
            birthdate = input('Date de naissance \'AAAA-MM-JJ\': ')
            new_player = {"ine": player_ine, "lastname": lastname, "name": name, "birthdate": birthdate}
            self.playermanager.addplayer(new_player)
            print(f'Joueur créé')
