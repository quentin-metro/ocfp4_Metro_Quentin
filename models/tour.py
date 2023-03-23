class Tour:
    """a Turn"""
    total_id_turn = 0

    def __init__(self, name: str, start_time: str, end_time: str, list_matchs, id_turn: int):
        self.id_turn = id_turn
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.list_matchs = list_matchs

    def endturn(self, date: str):
        self.end_time = date

    def getlistmatchs(self):
        return self.list_matchs

    def todict(self):
        my_dict = {'id_turn': self.id_turn,
                   'name': self.name,
                   'start_time': self.start_time,
                   'end_time': self.end_time,
                   'list_matchs': self.list_matchs
                   }
        return my_dict
