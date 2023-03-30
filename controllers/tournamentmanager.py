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
                id_tournament = int(float(tournoi['id_tournament']))
                if id_tournament >= self.total_id_tournament:
                    self.total_id_match = id_tournament

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
            if tournoi.getidtournament() == int(id_tournament):
                return tournoi

    def getinfotournament(self, id_tournament: int):
        """ Get the information of the tournament"""
        tournoi = self.selecttournament(id_tournament)
        if tournoi:
            return tournoi.todict()

    def getlistplayer(self, id_tournament: int):
        """ Get the list of player in the tournament"""
        tournoi = self.db.search(self.query.id_tournament == int(id_tournament))[0]
        list_player = tournoi['list_player']
        list_player_name = []
        for player_ine in list_player:
            player = self.playermanager.getplayerinfo(player_ine)[0]
            name = player['name']
            lastname = player['lastname']
            list_player_name.append((player_ine, lastname + ' ' + name))
        return list_player_name

    def getlistscore(self, id_tournament: int):
        """ Get the list of score in the tournament"""
        tournoi = self.db.search(self.query.id_tournament == int(id_tournament))[0]
        return tournoi['list_player_score']

    def getlistturn(self, id_tournament: int):
        """ Get list of turn from a tournament"""
        tournoi = self.db.search(self.query.id_tournament == int(id_tournament))[0]
        return tournoi['list_turns']

    def tournamentexist(self, name):
        list_tournoi = self.db.search(self.query.id_tournament.exists())
        for tournoi in list_tournoi:
            if name.casefold() == tournoi['name'].casefold():
                return False
        return True

    def addtournament(self, tournoi):
        """ Create a new tournament"""
        # Add incomplete value for a tournament
        self.total_id_tournament += 1
        tournoi['id_tournament'] = self.total_id_tournament
        tournoi['end_date'] = ""
        tournoi['current_turn'] = 0
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
                              tournoi['id_tournament'],
                              int(float(tournoi['turn_number'])),
                              int(float(tournoi['current_turn'])),
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
            current_turn = tournoi.getcurrentturnnumber()
            total_turn = tournoi.getturnnumber()
            time = DateHandler.getdatehours()
            if current_turn < total_turn:
                # Create the first turn
                if current_turn == 0:
                    number_of_player = len(tournoi.getlistplayer())
                    # Can't do a match if you don't have 2 player
                    if number_of_player % 2 != 0 or number_of_player == 0:
                        raise MyAppBadPlayerCount
                    else:
                        # Create list_player_score
                        list_player = tournoi.getlistplayer()
                        player_score = []
                        for player in list_player:
                            player_score.append((player, 0))
                        self.db.update({'list_player_score': player_score},
                                       (self.query.id_tournament == int(id_tournament)))
                        tournoi.editlistplayerscore(player_score)
                        # Create new turn
                        self.createnewturns(id_tournament, time)
                        current_turn = tournoi.advanceturn()
                        list_turns = tournoi.getlistturns()
                        list_turns_id = []
                        for turn in list_turns:
                            list_turns_id.append(turn)
                        # Update data
                        self.db.update({'list_turns': list_turns_id}, (self.query.id_tournament == int(id_tournament)))
                        self.db.update({'current_turn': current_turn}, (self.query.id_tournament == int(id_tournament)))
                        return True
                else:
                    # Check if all match are done
                    list_turns = tournoi.getlistturns()
                    # current_turn - 1 == index du dernier tour
                    list_matchs_id = self.turnmanager.getlistmatchs([list_turns[current_turn - 1]])
                    list_matchs = []
                    for match in list_matchs_id:
                        list_matchs.append(self.matchmanager.getmatch(match))
                    if self.matchmanager.gameover(list_matchs):
                        for match in list_matchs_id:
                            self.updatescore(id_tournament, match)
                        # Create a new turn
                        self.turnmanager.advanceturn(list_turns, time)
                        self.createnewturns(id_tournament, time)
                        current_turn = tournoi.advanceturn()
                        list_turns_id = []
                        for turn in list_turns:
                            list_turns_id.append(turn)
                        self.db.update({'list_turns': list_turns_id}, (self.query.id_tournament == int(id_tournament)))
                        self.db.update({'current_turn': current_turn}, (self.query.id_tournament == int(id_tournament)))
                        info_tournoi = self.db.search(self.query.id_tournament == int(id_tournament))[0]
                        player_score = info_tournoi['list_player_score']
                        self.db.update({'list_player_score': player_score},
                                       (self.query.id_tournament == int(id_tournament)))
                        return True
            else:
                # If last turn
                info_tournoi = self.db.search(self.query.id_tournament == int(id_tournament))[0]
                end_date = info_tournoi['end_date']
                if end_date != "":
                    return False
                # Check if all match are done
                list_turns = tournoi.getlistturns()
                # current_turn - 1 == index du dernier tour
                list_matchs_id = self.turnmanager.getlistmatchs([list_turns[current_turn - 1]])
                list_matchs = []
                for match in list_matchs_id:
                    list_matchs.append(self.matchmanager.getmatch(match))
                if self.matchmanager.gameover(list_matchs):
                    for match in list_matchs_id:
                        self.updatescore(id_tournament, match)
                    self.turnmanager.advanceturn(list_turns, time)
                    self.db.update({'end_date': time}, (self.query.id_tournament == int(id_tournament)))
                    tournoi.editenddate(time)
                    player_score = info_tournoi['list_player_score']
                    self.db.update({'list_player_score': player_score},
                                   (self.query.id_tournament == int(id_tournament)))
                return True
        else:
            return False

    """Create a new turn to the tournament"""
    def createnewturns(self, id_tournament: int, start_time: str):
        """ Create a new turn for this tournament - see advanceturn"""
        tournoi = self.selecttournament(id_tournament)
        if tournoi:
            # Create and sort a list of player+score who don't have a match for the turn
            info_tournoi = self.db.search(self.query.id_tournament == int(id_tournament))[0]
            unmatch_player_score = info_tournoi['list_player_score']
            # check if it is the first turn
            if tournoi.current_turn == 0:
                number_of_player = len(tournoi.getlistplayer())
                # Can't do a match if you don't have 2 player
                if number_of_player % 2 != 0 and number_of_player != 0:
                    raise MyAppBadPlayerCount
                # sort list_player_score by random
                random.shuffle(unmatch_player_score)
                match_already_done = []
            else:
                # sort list_player_score by the score
                unmatch_player_score.sort(key=lambda a: a[1])
                match_already_done = self.turnmanager.getlistmatchs(tournoi.list_turns)
            list_matchs = self.matchmanager.matchmaking(unmatch_player_score, match_already_done)
            list_match_id = []
            for match in list_matchs:
                list_match_id.append(self.matchmanager.getmatchid(match))
            # Create a new Tour instance
            turn_number = tournoi.current_turn
            turn_name = "Round" + str(turn_number + 1)
            new_turn = self.turnmanager.addturn(turn_name, start_time, list_match_id)
            tournoi.list_turns.append(self.turnmanager.getturnid(new_turn))

    def addplayer(self, id_tournament: int, player_ine):
        """ Add a player to the tournament"""
        if self.playermanager.exist(player_ine):
            tournoi = self.selecttournament(id_tournament)
            if tournoi:
                for player in tournoi.getlistplayer():
                    if player == player_ine:
                        raise MyAppAlreadyInException(player_ine)
                list_player = tournoi.getlistplayer()
                list_player.append(player_ine)
                self.db.update({'list_player': list_player}, (self.query.id_tournament == int(id_tournament)))
                tournoi.editlistplayer(list_player)
                return True
        else:
            raise MyAppPlayerNotFound(player_ine)

    def updatescore(self, id_tournament, id_match):
        tournoi = self.selecttournament(id_tournament)
        match = self.matchmanager.getmatchinfo(id_match)
        end_score = match['end_score']
        update_tournoi = self.db.search(self.query.id_tournament == int(id_tournament))[0]
        new_score_list = update_tournoi['list_player_score']
        for player in end_score:
            for player_score in new_score_list:
                if player[0] == player_score[0]:
                    player_score[1] = player_score[1] + player[1]
                    break
        self.db.update({'list_player_score': new_score_list}, self.query.id_tournament == int(id_tournament))
        tournoi.editlistplayerscore(new_score_list)
        return new_score_list

    def islastturn(self, id_tournament):
        tournoi = self.db.search(self.query.id_tournament == int(id_tournament))[0]
        if tournoi['turn_number'] == tournoi['current_turn']:
            return True
        else:
            return False

    def allmatchdone(self, id_tournament):
        tournoi = self.db.search(self.query.id_tournament == int(id_tournament))[0]
        list_matchs = self.turnmanager.getlistmatchs(tournoi['list_turns'])
        return self.matchmanager.gameover(list_matchs)
