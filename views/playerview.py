from controllers.playermanager import PlayerManager


class PlayerView:
    def __init__(self, playermanager: PlayerManager):
        self.playermanager = playermanager

    def askcommandplayer(self):
        while True:
            print(f'Quel action souhaitez vous effectuer?\n'
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
        playerlist = self.playermanager.getplayerlist()
        print(f'   INE   |  Nom Prenom | Date de Naissance')
        for player in playerlist:
            print(f'{player[0]} | {player[1]} {player[2]} | {player[4]}')

    def addplayer(self):
        player_ine = input('INE:')
        # Check if player_ine exist already in data and display the info
        player = self.playermanager.getplayerinfo(player_ine)
        if player:
            print(f'{player_ine} existe déjà\n'
                  f'{player[0]} | {player[1]} {player[2]} | {player[4]}')
            return
        lastname = input('Nom: ')
        name = input('Prenom: ')
        birthdate = input('Date de naissance \'AAAA-MM-JJ\': ')
        new_player = {"INE": player_ine, "lastname": lastname, "name": name, "birthdate": birthdate}
        self.playermanager.addplayer(new_player)
        print(f'Joueur créé')
