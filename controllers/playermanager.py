from models.joueur import Joueur
from controllers.manager import Manager
from controllers.myappexception import MyAppPlayerAlreadyExist, MyAppBadPlayerINE


class PlayerManager(Manager):
    """Control the Players"""

    def __init__(self):
        self.list_player = []
        self.list_missing = []
        # initialize the player list
        new_list_player = self.db.search(self.query.ine.exists())
        if new_list_player:
            for player in new_list_player:
                self.generateplayer(player)

    def getplayerlist(self):
        return self.list_player

    def getplayerlistindict(self):
        mylist = []
        for player in self.list_player:
            mylist.append(player.todict())
        return mylist

    def getplayerinfo(self, player_ine):
        return self.db.search(self.query.ine == player_ine)

    def addplayer(self, player):
        existant = self.db.search(self.query.ine == player['ine'])
        if not existant:
            new_player = self.generateplayer(player)
            self.db.insert(new_player.todict())
            for player_ine in self.list_missing:
                if player_ine == player['ine']:
                    self.list_missing.remove(player_ine)
            return True
        else:
            raise MyAppPlayerAlreadyExist

    def generateplayer(self, player):
        new_player = Joueur(player['ine'], player['lastname'], player['name'], player['birthdate'])
        self.list_player.append(new_player)
        return new_player

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

    @staticmethod
    def ineformat(player_ine):
        character_number = 1
        for character in player_ine:
            if character.isalpha() and character_number < 3:
                character_number += 1
            elif character.isdecimal() and 7 >= character_number >= 3:
                character_number += 1
            else:
                raise MyAppBadPlayerINE
