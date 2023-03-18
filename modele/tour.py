class Tour:
    """a Turn"""
    def __init__(self, name, start_time, end_time, list_matchs):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.list_matchs = list_matchs
        self.is_done = False

    def endturn(self):
        for match in self.list_matchs:
            if not match.is_done:
                quit()
        self.is_done = True
