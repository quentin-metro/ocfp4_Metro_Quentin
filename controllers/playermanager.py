from models.joueur import Joueur
from controllers.manager import Manager


class PlayerManager(Manager):
    """Control the Players"""

    def __init__(self):
        self.list_player = []
        self.list_missing = []
        # initialize the player list
        new_list_player = self.db.search(self.query.ine.exists())
        if new_list_player:
            for player in new_list_player:
                self.addplayer(player)

    def getplayerlist(self):
        return self.list_player

    def getplayerinfo(self, player_ine):
        return self.db.search(self.query.ine == player_ine)

    def addplayer(self, player):
        new_player = Joueur(player['INE'], player['lastname'], player['name'], player['birthdate'])
        self.list_player.append(new_player)
        self.db.insert(new_player.todict())
        for player_ine in self.list_missing:
            if player_ine == player['INE']:
                self.list_missing.remove(player_ine)
        return True

    def exist(self, player_ine: str):
        for know_player in self.list_player:
            if player_ine == know_player.ine:
                return True
        return False

    def missingplayer(self, list_player):
        for player_ine in list_player:
            if player_ine:
                if not self.exist(player_ine):
                    self.list_missing.append(player_ine)
        return self.list_missing
