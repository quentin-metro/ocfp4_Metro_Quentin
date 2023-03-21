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
        # check if it is the first turn or sort list_player_score by the score
        if self.current_turn == 0:
            random.shuffle(unmatch_player_score)
        else:
            unmatch_player_score.sort(key=lambda a: a[1])
        # Match player for a match
        for player_score in unmatch_player_score:
            unmatch_player_score.remove(player_score)
            all_match_done = True
            # Looking for other player to match
            for player_to_match in unmatch_player_score:
                matched_player_score = (player_score, player_to_match)
                new_match = match.Match(matched_player_score)
                # Verify if a match exists in previous turn
                match_already_done = False
                for turn in self.list_turns:
                    if turn.matchdone(new_match):
                        match_already_done = True
                        break
                if match_already_done:
                    del new_match
                else:
                    list_matchs.append(new_match)
                    unmatch_player_score.remove(player_to_match)
                    break
            # IF all match already done once , randomize a match
            if all_match_done:
                random_player = random.choice(unmatch_player_score)
                matched_player_score = (player_score, random_player)
                new_match = match.Match(matched_player_score)
                list_matchs.append(new_match)
                unmatch_player_score.remove(random_player)

        # Create a new Tour instance
        turn_name = "Round" + str(self.current_turn)
        new_turn = tour.Tour(turn_name, start_time, end_time, list_matchs)
        self.list_turns.append(new_turn)

    """Advance a new turn to the tournament"""
    def advanceturn(self, start_time, end_time):
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
