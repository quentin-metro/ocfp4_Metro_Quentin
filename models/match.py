class Match:
    """a match"""
    total_id_match = 0

    # player_score, winner_score == (player, score)
    # matched_player_score == ([player1, score1],[player2, score2])
    def __init__(self, matched_player_score, id_match: int = None):
        self.id_match = 0
        self.editidmatch(id_match)
        self.total_id_match += 1
        self.id_match = self.total_id_match
        self.matched_player_score = matched_player_score
        self.player_score1 = matched_player_score[0]
        self.player_score2 = matched_player_score[1]
        self.is_over = False
        self.end_score = []

    def editidmatch(self, id_match=None):
        if id_match is None:
            self.total_id_match += 1
            self.id_match = self.total_id_match
        else:
            self.id_match = id_match
            if id_match > self.total_id_match:
                self.total_id_match = id_match
        return True

    def win(self, winner):
        # if match is a win , and change the tournament score of the player
        self.is_over = True
        if winner == self.player_score1[0]:
            self.player_score1[1] += 1
        else:
            self.player_score2[1] += 1
        self.end_score = [self.player_score1, self.player_score2]
        return self.end_score

    def draw(self):
        # if match is a draw , and change the tournament score of the player
        self.player_score1[1] += 0.5
        self.player_score2[1] += 0.5
        self.is_over = False
        self.end_score = [self.player_score1, self.player_score2]
        return self.end_score

    def samematch(self, new_match):
        # Check if the match is the same in any order
        match_already_done = self.matched_player_score
        if match_already_done == new_match or match_already_done == new_match[::-1]:
            return True
        else:
            return False
