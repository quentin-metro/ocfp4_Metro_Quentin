class Match:
    """a match"""

    # player_score, winner_score = (player, score)
    def __init__(self, matched_player_score):
        self.matched_player_score = matched_player_score
        self.player_score1 = matched_player_score[0]
        self.player_score2 = matched_player_score[1]
        self.is_over = False

    def win(self, winner):
        # if match is a win , and change the tournament score of the player
        self.is_over = True
        if winner == self.player_score1[0]:
            self.player_score1[1] += 1
            return self.player_score1
        else:
            self.player_score2[1] += 1
            return self.player_score2

    def draw(self):
        # if match is a draw , and change the tournament score of the player
        self.player_score1[1] += 0.5
        self.player_score2[1] += 0.5
        self.is_over = False
        return [self.player_score1, self.player_score2]

    def samematch(self, new_match):
        # Check if the match is the same in any order
        match_already_done = self.matched_player_score
        if match_already_done == new_match or match_already_done == new_match[::-1]:
            return True
        else:
            return False
