import random
from controllers.myappexception import *
from models.tournoi import Tournoi
from controllers.playermanager import PlayerManager
from controllers.matchmanager import MatchManager
from controllers.turnmanager import TurnManager
from controllers.manager import Manager


class TournamentManager(Manager):
    """Control the Tournaments"""
    def __init__(self):
        self.list_tournament = []
        self.total_id_tournament = 0
        self.playermanager = PlayerManager()
        self.turnmanager = TurnManager()
        self.matchmanager = MatchManager()
        # initialize the tournament list
        new_list_tournament = self.db.search(self.query.id_tournament.exists())
        if new_list_tournament:
            for tournoi in new_list_tournament:
                self.createtournament(tournoi)

    def getplayermanager(self):
        return self.playermanager

    def gettotalidtournament(self):
        return self.total_id_tournament

    def getlisttournament(self, state=None):
        if state is None:
            return self.db.search(self.query.id_tournament.exists())
        elif state:
            return self.db.search(self.query.state_tournament == 'True')
        else:
            return self.db.search(self.query.state_tournament == 'False')

    def selecttournament(self, id_tournament: int):
        for tournoi in self.list_tournament:
            if tournoi.getidtournament() == id_tournament:
                return tournoi

    def getinfotournament(self, id_tournament: int):
        tournoi = self.selecttournament(id_tournament)
        return tournoi.todict()

    def getlistplayer(self, id_tournament: int):
        tournoi = self.db.search(self.query.id_tournament == id_tournament)
        # tournoi[7] is list of player for a tournament
        listplayer = tournoi[7]
        list_player_name = []
        for player_ine in listplayer:
            player = self.playermanager.getplayerinfo(player_ine)
            name = player['name']
            lastname = player['lastname']
            list_player_name.append((player_ine, lastname + ' ' + name))
        return list_player_name

    def getlistturn(self, id_tournament: int):
        tournoi = self.db.search(self.query.id_tournament == id_tournament)
        # tournoi[9] is list of turns for a tournament
        return tournoi[9]

    def addtournament(self, tournoi):
        new_tournoi = self.createtournament(tournoi)
        self.db.insert(new_tournoi.todict())

    def createtournament(self, tournoi):
        new_tournament_id = int(float(tournoi['id_tournament']))
        if not new_tournament_id:
            self.total_id_tournament += 1
            new_tournament_id = self.total_id_tournament
        new_tournoi = Tournoi(tournoi['name'],
                              tournoi['place'],
                              tournoi['start_date'],
                              tournoi['end_date'],
                              tournoi['desc'],
                              tournoi['state_tournament'],
                              int(float(tournoi['turn_number'])),
                              int(float(tournoi['current_turn'])),
                              new_tournament_id,
                              tournoi['list_turns'],
                              tournoi['list_player'],
                              tournoi['list_player_score']
                              )
        self.list_tournament.append(new_tournoi)
        return new_tournoi

    """Create a new turn to the tournament"""
    def createnewturns(self, id_tournament: int, start_time: str):
        tournoi = self.selecttournament(id_tournament)
        if tournoi:
            # Create and sort a list of player+score who don't have a match for the turn
            unmatch_player_score = tournoi.list_player_score
            # check if it is the first turn or sort list_player_score by the score
            if tournoi.current_turn == 0:
                number_of_player = tournoi.getlistplayer().len()
                if number_of_player % 2 != 0:
                    raise MyAppBadPlayerCount
                random.shuffle(unmatch_player_score)
            else:
                unmatch_player_score.sort(key=lambda a: a[1])
            match_already_done = self.turnmanager.getlistmatchs(tournoi.list_turns)
            list_matchs = self.matchmanager.matchmaking(unmatch_player_score, match_already_done)

            # Create a new Tour instance
            turn_number = tournoi.current_turn
            turn_name = "Round" + str(turn_number)
            new_turn = self.turnmanager.addturn(turn_name, start_time, list_matchs)
            tournoi.list_turns.append(new_turn)

    def advanceturn(self, id_tournament: int, time: str):
        tournoi = self.selecttournament(id_tournament)
        if tournoi:
            current_turn = tournoi.getcurrentturn()
            total_turn = tournoi.getturnnumber()
            if current_turn < total_turn:
                list_turns = tournoi.list_turns()
                list_matchs = self.turnmanager.getlistmatchs(list_turns)
                if self.matchmanager.gameover(list_matchs):
                    self.turnmanager.advanceturn(list_turns, time)
                    if current_turn == total_turn:
                        self.createnewturns(id_tournament, time)

    def addplayer(self, id_tournament: int, player_ine):
        if self.playermanager.exist(player_ine):
            tournoi = self.selecttournament(id_tournament)
            if tournoi:
                for player in tournoi.getlistplayer():
                    if player == player_ine:
                        raise MyAppAlreadyINException(player_ine)
                return True
        else:
            raise MyAppPlayerNotFound(player_ine)
