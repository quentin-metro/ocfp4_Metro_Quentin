import random
from models.match import Match
from controllers.manager import Manager


class MatchManager(Manager):

    """Control the Tournaments"""
    def __init__(self):
        self.list_matchs = []
        self.total_id_match = 0
        # initialize the match list
        new_list_match = self.db.search(self.query.id_match.exists())
        if new_list_match:
            for match in new_list_match:
                self.creatematch(match)
                match_id = int(float(match['id_match']))
                if match_id > self.total_id_match:
                    self.total_id_match = match_id

    def creatematch(self, match):
        new_match_id = int(float(match['id_match']))
        if not new_match_id:
            new_match_id = self.total_id_match + 1
        new_match = Match(match['matched_player_score'],
                          new_match_id,
                          match['end_score']
                          )
        self.list_matchs.append(new_match)
        return new_match

    def addmatch(self, match):
        new_match = self.creatematch(match)
        self.db.insert(new_match.todict())
        return new_match

    def matchmaking(self, unmatch_player_score, list_match_done):
        list_matchs = []
        # Match player for a match
        for player_score in unmatch_player_score:
            unmatch_player_score.remove(player_score)
            all_match_done = True
            # Looking for other player to match
            for player_to_match in unmatch_player_score:
                matched_player_score = (player_score, player_to_match)
                # Verify if a match exists in previous turn
                if not self.matchdone(matched_player_score, list_match_done):
                    new_matched = {"matched_player_score": matched_player_score}
                    new_match = self.addmatch(new_matched)
                    list_matchs.append(new_match)
                    unmatch_player_score.remove(player_to_match)
                    break
            # IF all match already done once , randomize a match
            if all_match_done:
                random_player = random.choice(unmatch_player_score)
                matched_player_score = (player_score, random_player)
                new_match = self.addmatch(matched_player_score)
                list_matchs.append(new_match)
                unmatch_player_score.remove(random_player)

    def win(self, match, winner):
        start_score = match.getmatchedplayerscore()
        if winner == start_score[0]:
            start_score[0][1] += 1
        else:
            start_score[1][1] += 1
        game_over = match.endmatch(start_score)
        self.db.update(match.todict(), self.query.id_match == match.getidmatch())
        return game_over

    def draw(self, match):
        start_score = match.getmatchedplayerscore()
        start_score[0][1] += 0.5
        start_score[0][1] += 0.5
        game_over = match.endmatch(start_score)
        self.db.update(match.todict(), self.query.id_match == match.getidmatch())
        return game_over

    @staticmethod
    def gameover(list_matchs):
        for match in list_matchs:
            if not match.getendscore():
                return False
        return True

    @staticmethod
    def matchdone(new_matched_player_score, list_match_done):
        # check if a new match exist in this turn
        for match_already_done in list_match_done:
            if match_already_done.samematch(new_matched_player_score):
                return True
        return False
