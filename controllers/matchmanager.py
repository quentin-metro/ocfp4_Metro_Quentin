import random
from models.match import Match
from controllers.manager import Manager
from controllers.myappexception import MyAppDontPlayThisMatch


class MatchManager(Manager):

    """Control the Tournaments"""
    def __init__(self):
        self.list_matchs = []
        self.total_id_match = 0
        # initialize the match list
        new_list_match = self.db.search(self.query.id_match.exists())
        if new_list_match:
            for match in new_list_match:
                id_match = int(float(match['id_match']))
                new_match = Match(match['matched_player_score'],
                                  id_match,
                                  match['end_score']
                                  )
                self.list_matchs.append(new_match)
                if id_match >= self.total_id_match:
                    self.total_id_match = id_match

    def getmatch(self, match_id):
        for match in self.list_matchs:
            if match.getidmatch() == match_id:
                return match

    def getmatchinfo(self, id_match):
        return self.db.search(self.query.id_match == int(id_match))[0]

    def creatematch(self, matched):
        self.total_id_match += 1
        new_match_id = self.total_id_match
        new_match = Match(matched,
                          new_match_id
                          )
        return new_match

    def matchmaking(self, unmatch_player_score, list_match_done):
        list_matchs = []
        # Match player for a match
        for player_score in unmatch_player_score:
            unmatch_player_score.remove(player_score)
            all_match_done = True
            if list_match_done:
                # Looking for other player to match
                for player_to_match in unmatch_player_score:
                    matched_player_score = [(player_score[0], 0), (player_to_match[0], 0)]
                    # Verify if a match exists in previous turn
                    if not self.matchdone(matched_player_score, list_match_done):
                        new_match = self.creatematch(matched_player_score)
                        list_matchs.append(new_match)
                        unmatch_player_score.remove(player_to_match)
                        all_match_done = False
                        self.list_matchs.append(new_match)
                        self.db.insert(new_match.todict())
                        break
            # IF all match already done once or first turn, randomize a match
            if all_match_done:
                random_player = random.choice(unmatch_player_score)
                matched_player_score = [(player_score[0], 0), (random_player[0], 0)]
                new_match = self.creatematch(matched_player_score)
                list_matchs.append(new_match)
                unmatch_player_score.remove(random_player)
                self.list_matchs.append(new_match)
                self.db.insert(new_match.todict())
        return list_matchs

    def win(self, match_id, winner):
        match = self.getmatch(match_id)
        start_score = match.getmatchedplayerscore()
        if winner == start_score[0][0]:
            end_score = [(start_score[0][0], start_score[0][1] + 1), (start_score[1][0], start_score[1][1])]
        elif winner == start_score[1][0]:
            end_score = [(start_score[0][0], start_score[0][1]), (start_score[1][0], start_score[1][1] + 1)]
        else:
            raise MyAppDontPlayThisMatch
        game_over = match.endmatch(end_score)
        self.db.update(match.todict(), self.query.id_match == match.getidmatch())
        return game_over

    def draw(self, match_id):
        match = self.getmatch(match_id)
        start_score = match.getmatchedplayerscore()
        end_score = [(start_score[0][0], start_score[0][1] + 0.5), (start_score[1][0], start_score[1][1] + 0.5)]
        game_over = match.endmatch(end_score)
        self.db.update(match.todict(), self.query.id_match == match.getidmatch())
        return game_over

    def matchdone(self, new_matched_player_score, list_match_done):
        # check if a new match exist in this turn
        for match_already_done in list_match_done:
            match = self.getmatch(match_already_done)
            if match.samematch(new_matched_player_score):
                return True
        return False

    def gameover(self, list_matchs):
        for match_id in list_matchs:
            if type(match_id) == Match:
                match = match_id
            else:
                match = self.getmatch(match_id)
            if match.getendscore() is None:
                return False
        return True

    @staticmethod
    def getmatchid(match: Match):
        return match.id_match

    @staticmethod
    def readablescore(score):
        # score = [(player1,score1),(player2,score2)]
        return f'{score[0][0]} {score[0][1]} : {score[1][1]} {score[1][0]}'

    @staticmethod
    def getwinner(start_score, end_score):
        if end_score[0][1] == start_score[0][1] + 0.5:
            return "Draw"
        elif end_score[0][1] != start_score[0][1]:
            return end_score[0][0]
        else:
            return end_score[1][0]
