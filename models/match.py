class Match:
    """a match"""
    total_id_match = 0

    # player_score, winner_score == (player, score)
    # matched_player_score == ([player_ine1, score1],[player_ine2, score2])
    def __init__(self, matched_player_score, id_match: int, end_score=None):
        self.id_match = id_match
        self.matched_player_score = matched_player_score
        self.end_score = end_score

    def getidmatch(self):
        return self.id_match

    def getmatchedplayerscore(self):
        return self.matched_player_score

    def getendscore(self):
        return self.end_score

    def endmatch(self, end_score):
        self.end_score = end_score

    def samematch(self, new_matched_player_score):
        # Check if the match is the same in any order
        match_already_done = self.matched_player_score
        if match_already_done == new_matched_player_score or match_already_done == new_matched_player_score[::-1]:
            return True
        else:
            return False

    def todict(self):
        my_dict = {'id_match': self.id_match,
                   'matched_player_score': self.matched_player_score,
                   'end_score': self.end_score,
                   }
        return my_dict
