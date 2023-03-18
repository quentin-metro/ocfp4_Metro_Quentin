class Match:
    """a match"""

    # player_score, winner_score = (player, score)
    def __init__(self, matched_player_score):
        self.player_score1 = matched_player_score[0]
        self.player_score2 = matched_player_score[1]
        self.is_done = False

    def win(self, winner):
        self.is_done = True
        if winner == self.player_score1[0]:
            self.player_score1[1] += 1
            return self.player_score1
        else:
            self.player_score2[1] += 1
            return self.player_score2

    def draw(self):
        self.player_score1[1] += 0.5
        self.player_score2[1] += 0.5
        self.is_done = False
        return [self.player_score1, self.player_score2]
