import random
from .tour import Tour
from controler.matchmaking import matchmaking


class Tournoi:
    """a Tournament"""
    total_id_tournament = 0

    def __init__(self, name: str, place: str, start_date: str, end_date: str, list_players, desc_tournament, list_turn,
                 turn_number=4, current_turn=0, list_player_score=None, id_tournament: int = None):
        self.id_tournament = 0
        self.editidtournament(id_tournament)
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.turn_number = turn_number
        self.desc_tournament = desc_tournament
        self.list_player = list_players
        self.list_turns = list_turn
        self.current_turn = current_turn
        if list_player_score is None:
            self.list_player_score = []
            for player in list_players:
                # connect a player and a score in the tournament
                self.list_player_score.append([player, 0])
        else:
            self.list_player_score = list_player_score

    def editidtournament(self, id_tournament: int = None):
        if id_tournament is None:
            self.total_id_tournament += 1
            self.id_tournament = self.total_id_tournament
        else:
            self.id_tournament = id_tournament
            if id_tournament > self.total_id_tournament:
                self.total_id_tournament = id_tournament

    def editlistplayer(self, list_players):
        self.list_player = list_players
        return self.list_player

    """Create a new turn to the tournament"""
    def createturns(self, start_time: str, end_time: str):
        # Create and sort a list of player+score who don't have a match for the turn
        unmatch_player_score = self.list_player_score
        # check if it is the first turn or sort list_player_score by the score
        if self.current_turn == 0:
            random.shuffle(unmatch_player_score)
        else:
            unmatch_player_score.sort(key=lambda a: a[1])
        list_matchs = matchmaking(unmatch_player_score, self.list_turns)

        # Create a new Tour instance
        turn_name = "Round" + str(self.current_turn)
        new_turn = Tour(turn_name, start_time, end_time, list_matchs)
        self.list_turns.append(new_turn)

    """Advance a new turn to the tournament"""
    def advanceturn(self, start_time: str, end_time: str):
        # finish precedent turn and create a new one or end the tournament if already last turn
        if self.current_turn != self.turn_number:
            self.current_turn += 1
            self.createturns(start_time, end_time)
            return True
        else:
            return False

    """End the tournament"""
    def endtournament(self):
        # End the tournament if all turn are over
        for turn in self.list_turns:
            if turn.is_over:
                return False
        return True

    def todir(self):
        my_dir = {'id_tournament': self.id_tournament,
                  'name': self.name,
                  'place': self.place,
                  'start date': self.start_date,
                  'end date': self.end_date,
                  'turn number': self.turn_number,
                  'desc': self.desc_tournament,
                  'list player': self.list_player,
                  'list player score': self.list_player_score,
                  'list turns': self.list_turns,
                  'current turn': self.current_turn
                  }
        return my_dir
