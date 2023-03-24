class Tournoi:
    """a Tournament"""

    def __init__(self, name: str, place: str, start_date: str, end_date: str,
                 desc_tournament: str, state_tournament: bool,
                 id_tournament: int, turn_number: int = 4, current_turn: int = 0, list_turn=None,
                 list_players=None, list_player_score=None):
        self.id_tournament = id_tournament
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.turn_number = turn_number
        self.desc_tournament = desc_tournament
        self.list_player = list_players
        self.list_turns = list_turn
        self.current_turn = current_turn
        self.state_tournament = state_tournament
        if list_player_score is None:
            self.list_player_score = []
            for player in list_players:
                # connect a player and a score in the tournament
                self.list_player_score.append([player, 0])
        else:
            self.list_player_score = list_player_score

    def getidtournament(self):
        return self.id_tournament

    def getlistplayer(self):
        return self.list_player

    def editlistplayer(self, list_players: list):
        self.list_player = list_players
        return self.list_player

    def getlistturns(self):
        return self.list_turns

    def editlistturn(self, new_list_turn: list):
        self.list_turns = new_list_turn

    def addturn(self, new_turn: list):
        self.list_turns.append(new_turn)

    def getcurrentturnnumber(self):
        return self.current_turn

    def getturnnumber(self):
        return self.turn_number

    """Advance a new turn to the tournament"""
    def advanceturn(self):
        # finish precedent turn and create a new one or end the tournament if already last turn
        if self.current_turn != self.turn_number:
            self.current_turn += 1
            return True
        else:
            self.state_tournament = True
            return False

    """End the tournament"""
    def endtournament(self):
        # End the tournament if all turn are over
        for turn in self.list_turns:
            if turn.is_over:
                return False
        self.state_tournament = True
        return True

    def todict(self):
        my_dict = {'id_tournament': self.id_tournament,
                   'name': self.name,
                   'place': self.place,
                   'start date': self.start_date,
                   'end date': self.end_date,
                   'turn number': self.turn_number,
                   'desc': self.desc_tournament,
                   'list player': self.list_player,
                   'list player score': self.list_player_score,
                   'list turns': self.list_turns,
                   'current turn': self.current_turn,
                   'state_tournament': self.state_tournament
                   }
        return my_dict
