class Tour:
    """a Turn"""
    def __init__(self, name, start_time, end_time, list_matchs):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.list_matchs = list_matchs
        self.is_over = False

    def endturn(self):
        # check if all match is over
        all_matchs_over = True
        for match in self.list_matchs:
            if not match.is_over:
                all_matchs_over = False
                break
        if all_matchs_over:
            self.is_over = True
            return True
        else:
            return False

    def matchdone(self, new_match):
        # check if a new match exist in this turn
        for match_already_done in self.list_matchs:
            if match_already_done.samematch(new_match):
                return True
        return False
