class Tour:
    """a Turn"""
    total_id_turn = 0

    def __init__(self, name: str, start_time: str, end_time: str, list_matchs, id_turn: int = None):
        self.id_turn = 0
        self.editidturn(id_turn)
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

    def editidturn(self, id_turn=None):
        if id_turn is None:
            self.total_id_turn += 1
            self.id_turn = self.total_id_turn
        else:
            self.id_turn = id_turn
            if id_turn > self.total_id_turn:
                self.total_id_turn = id_turn
        return True
