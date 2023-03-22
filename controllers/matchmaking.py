import random
from models.match import Match
# from models.tour import Tour


def matchmaking(unmatch_player_score, list_turns):
    list_matchs = []
    # Match player for a match
    for player_score in unmatch_player_score:
        unmatch_player_score.remove(player_score)
        all_match_done = True
        # Looking for other player to match
        for player_to_match in unmatch_player_score:
            matched_player_score = (player_score, player_to_match)
            new_match = Match(matched_player_score)
            # Verify if a match exists in previous turn
            match_already_done = False
            for turn in list_turns:
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
            new_match = Match(matched_player_score)
            list_matchs.append(new_match)
            unmatch_player_score.remove(random_player)
