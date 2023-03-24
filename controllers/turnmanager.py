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

    def getinfoturn(self, id_turn):
        return self.db.search(self.query.id_turn == id_turn)

    def createturn(self, turn):
        new_turn_id = int(float(turn['id_turn']))
        new_tour = Tour(turn['name'],
                        turn['start_time'],
                        turn['end_time'],
                        turn['liste_matchs'],
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

    def endturn(self, turn_id, end_time: str):
        for turn in self.list_turn:
            if turn['id_turn'] == turn_id:
                turn_over = turn.endturn(end_time)
                self.db.update(turn.todict(), self.query.id_turn == turn_id)
                return turn_over

    @staticmethod
    def advanceturn(turn_list, end_time: str):
        for turn in turn_list:
            if not turn['end_time']:
                turn.endturn(turn['id_turn'], end_time)

    @staticmethod
    def getlistmatchs(list_turn):
        list_matchs = []
        for turn in list_turn:
            list_matchs.append(turn.getlistmatchs())
        return list_matchs
