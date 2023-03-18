import match
import tour
import random


class Tournoi:
    """a Tournament"""

    # list_turns

    def __init__(self, name, place, start_date, end_date,
                 list_players, desc_tournament, turn_number=4):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.turn_number = turn_number
        self.desc_tournament = desc_tournament
        self.list_player_score = []
        self.list_turns = []
        self.current_turn = 0
        for player in list_players:
            # connect a player and a score in the tournament
            self.list_player_score.append((player, 0))

    """Create a new turn to the tournament"""
    def createturns(self, start_time, end_time):
        list_matchs = []
        # Create and sort a list of player+score who don't have a match for the turn
        unmatch_player_score = self.list_player_score
        if self.current_turn == 0:
            random.shuffle(unmatch_player_score)
        else:
            unmatch_player_score.sort(key=lambda a: a[1])
        # Match player for a match
        for player_score in unmatch_player_score:
            unmatch_player_score.remove(player_score)
            matched_player_score = (player_score, unmatch_player_score[0])
            new_match = match.Match(matched_player_score)
            list_matchs.append(new_match)
        # Create a new Tour instance
        turn_name = "Round" + str(self.current_turn)
        new_turn = tour.Tour(turn_name, start_time, end_time, list_matchs)
        self.list_turns.append(new_turn)

    """Advance a new turn to the tournament"""
    def advanceturn(self, start_time, end_time):
        if self.current_turn != self.turn_number:
            self.current_turn += 1
            self.createturns(start_time, end_time)
        else:
            self.endtournament()

    """End the tournament"""
    def endtournament(self):
        print(f"Tournoi fini")
        return self.list_player_score
