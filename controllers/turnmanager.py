from models.tour import Tour
from controllers.manager import Manager


class TurnManager(Manager):

    def __init__(self):
        self.total_turn_id = 0
        self.list_turn = []
        new_list_turn = self.db.search(self.query.id_turn.exists())
        if new_list_turn:
            for turn in new_list_turn:
                self.createturn(turn)

    def getturn(self, turn_id):
        for turn in self.list_turn:
            if turn.getturnid() == int(turn_id):
                return turn

    def getinfoturn(self, id_turn):
        return self.db.search(self.query.id_turn == int(id_turn))[0]

    def createturn(self, turn):
        new_turn_id = int(float(turn['id_turn']))
        new_tour = Tour(turn['name'],
                        turn['start_time'],
                        turn['end_time'],
                        turn['list_matchs'],
                        new_turn_id
                        )
        self.list_turn.append(new_tour)
        self.total_turn_id += 1
        return new_tour

    def addturn(self, turn_name, start_time, list_matchs):
        turn = {'name': turn_name, 'start_time': start_time, 'end_time': None,
                'list_matchs': list_matchs, 'id_turn': self.total_turn_id}
        new_turn = self.createturn(turn)
        self.db.insert(new_turn.todict())
        return new_turn

    def advanceturn(self, turn_list, end_time: str):
        for turn_id in turn_list:
            turn_info = self.getinfoturn(turn_id)
            if turn_info['end_time'] is None:
                turn = self.getturn(turn_id)
                turn.endturn(end_time)
                self.endturn(turn_info['id_turn'], end_time)

    def endturn(self, turn_id, end_time: str):
        for turn in self.list_turn:
            if turn.getturnid() == int(turn_id):
                turn_over = turn.endturn(end_time)
                self.db.update(turn.todict(), self.query.id_turn == int(turn_id))
                return turn_over

    def getlistmatchs(self, list_turn_id):
        list_matchs = []
        for turn_id in list_turn_id:
            turn = self.getturn(turn_id)
            for match in turn.getlistmatchs():
                list_matchs.append(match)
        return list_matchs

    @staticmethod
    def getturnid(turn: Tour):
        return turn.getturnid()
