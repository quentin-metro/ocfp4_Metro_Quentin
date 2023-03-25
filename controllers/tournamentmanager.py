import random
from controllers.myappexception import *
from models.tournoi import Tournoi
from controllers.playermanager import PlayerManager
from controllers.matchmanager import MatchManager
from controllers.turnmanager import TurnManager
from controllers.manager import Manager
from controllers.datehandler import DateHandler


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
        """ Get a list of tournament"""
        if state is None:
            """ All the tournaments """
            return self.db.search(self.query.id_tournament.exists())
        elif state:
            """ All the running tournaments"""
            return self.db.search(self.query.state_tournament == 'True')
        else:
            """ All the finished tournaments"""
            return self.db.search(self.query.state_tournament == 'False')

    def selecttournament(self, id_tournament: int):
        """ Select a specific tournament instance"""
        for tournoi in self.list_tournament:
            if tournoi.getidtournament() == id_tournament:
                return tournoi

    def getinfotournament(self, id_tournament: int):
        """ Get the information of the tournament"""
        tournoi = self.selecttournament(id_tournament)
        return tournoi.todict()

    def getlistplayer(self, id_tournament: int):
        """ Get the list of player in the tournament"""
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
        """ Get list of turn from a tournament"""
        tournoi = self.db.search(self.query.id_tournament == id_tournament)
        # tournoi[9] is list of turns for a tournament
        return tournoi[9]

    def addtournament(self, tournoi):
        """ Create a new tournament"""
        # Add incomplete value for a tournament
        self.total_id_tournament += 1
        tournoi['id_tournament'] = self.total_id_tournament
        tournoi['end_date'] = ""
        tournoi['current_turn'] = 1
        tournoi['state_tournament'] = "True"
        tournoi['list_turns'] = []
        tournoi['list_player'] = []
        tournoi['list_player_score'] = []
        # Create a tournament
        new_tournoi = self.createtournament(tournoi)
        self.db.insert(new_tournoi.todict())
        return new_tournoi.getidtournament()

    def createtournament(self, tournoi):
        """ Create a tournament instance"""
        new_tournoi = Tournoi(tournoi['name'],
                              tournoi['place'],
                              tournoi['start_date'],
                              tournoi['end_date'],
                              tournoi['desc'],
                              tournoi['state_tournament'],
                              int(float(tournoi['turn_number'])),
                              int(float(tournoi['current_turn'])),
                              tournoi['id_tournament'],
                              tournoi['list_turns'],
                              tournoi['list_player'],
                              tournoi['list_player_score']
                              )
        self.list_tournament.append(new_tournoi)
        return new_tournoi

    def advanceturn(self, id_tournament: int):
        """ Handle creating a new turn for this tournament"""
        tournoi = self.selecttournament(id_tournament)
        if tournoi:
            # Compare turn current and turn max
            current_turn = tournoi.getcurrentturn()
            total_turn = tournoi.getturnnumber()
            if current_turn < total_turn:
                time = DateHandler.getdatehours()
                # Create the first turn
                if current_turn == 1:
                    number_of_player = tournoi.getlistplayer().len()
                    # Can't do a match if you don't have 2 player
                    if number_of_player % 2 != 0 or number_of_player == 0:
                        raise MyAppBadPlayerCount
                    else:
                        self.createnewturns(id_tournament, time)
                        return True
                # Check if all match are done
                list_turns = tournoi.list_turns()
                list_matchs = self.turnmanager.getlistmatchs(list_turns)
                if self.matchmanager.gameover(list_matchs):
                    # Create a new turn
                    self.turnmanager.advanceturn(list_turns, time)
                    return True
        else:
            return False

    """Create a new turn to the tournament"""
    def createnewturns(self, id_tournament: int, start_time: str):
        """ Create a new turn for this tournament - see advanceturn"""
        tournoi = self.selecttournament(id_tournament)
        if tournoi:
            # Create and sort a list of player+score who don't have a match for the turn
            unmatch_player_score = tournoi.list_player_score
            # check if it is the first turn
            if tournoi.current_turn == 0:
                number_of_player = tournoi.getlistplayer().len()
                # Can't do a match if you don't have 2 player
                if number_of_player % 2 != 0 and number_of_player != 0:
                    raise MyAppBadPlayerCount
                # sort list_player_score by random
                random.shuffle(unmatch_player_score)
            else:
                # sort list_player_score by the score
                unmatch_player_score.sort(key=lambda a: a[1])
            match_already_done = self.turnmanager.getlistmatchs(tournoi.list_turns)
            list_matchs = self.matchmanager.matchmaking(unmatch_player_score, match_already_done)

            # Create a new Tour instance
            turn_number = tournoi.current_turn
            turn_name = "Round" + str(turn_number)
            new_turn = self.turnmanager.addturn(turn_name, start_time, list_matchs)
            tournoi.list_turns.append(new_turn)

    def addplayer(self, id_tournament: int, player_ine):
        """ Add a player to the tournament"""
        if self.playermanager.exist(player_ine):
            tournoi = self.selecttournament(id_tournament)
            if tournoi:
                for player in tournoi.getlistplayer():
                    if player == player_ine:
                        raise MyAppAlreadyINException(player_ine)
                return True
        else:
            raise MyAppPlayerNotFound(player_ine)

    def updatescore(self, id_tournament, id_match):
        tournoi = self.selecttournament(id_tournament)
        match = self.matchmanager.getmatchinfo(id_match)
        end_score = match['end_score']
        update_tournoi = self.db.search(self.query.id_tournament == id_tournament)
        new_score_list = update_tournoi['list_player_score']
        for player in end_score:
            for player_score in new_score_list:
                if player == player_score[0]:
                    player_score[1] = player[1]
                    break
        self.db.update({'list_player_score': new_score_list}, (self.query.id_tournament == id_tournament))
        tournoi.editlistplayerscore(new_score_list)

    def islastturn(self, id_tournament):
        tournoi = self.db.search(self.query.id_tournament == id_tournament)
        if tournoi['turn_number'] == tournoi['current_turn']:
            return True
        else:
            return False

    def allmatchdone(self, id_tournament):
        tournoi = self.db.search(self.query.id_tournament == id_tournament)
        list_matchs = self.turnmanager.getlistmatchs(tournoi['list_turns'])
        return self.matchmanager.gameover(list_matchs)
