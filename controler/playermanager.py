import json
from modele.joueur import Joueur


class PlayerManager:
    list_player = []
    """Control the Players"""
    def __init__(self):
        self.list_player = []
        # initialize the player list
        try:
            with open('./data/player.json', 'r') as player_file:
                player_json = json.load(player_file)
                for player in player_json:
                    self.addplayer(player)
                player_file.close()

        except FileNotFoundError:
            pass

    def addplayer(self, player):
        new_player = Joueur(player['INE'],
                            player.get('lastname'),
                            player.get('name'),
                            player.get('birthdate'),
                            )
        self.list_player.append(new_player)
        return True

    def exist(self, player_ine: str):
        for player in self.list_player:
            if player_ine == player['INE']:
                return True
        return False

    def tojson(self):
        # Write the player in json
        with open('./data/player.json', 'w', encoding='utf-8') as player_file:
            json.dump(self.list_player, player_file, indent=4)
            player_file.close()
