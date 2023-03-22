import json
from models.tournoi import Tournoi
from controllers.playermanager import PlayerManager


class TournamentManager:
    list_tournament = []
    """Control the Tournaments"""
    def __init__(self):
        self.list_tournament = []
        # initialize the tournament list
        try:
            with open('./data/tournoi.json', 'r') as tournoi_file:
                tournoi_json = json.load(tournoi_file)
                for tournoi in tournoi_json:
                    self.newtournament(tournoi)
                tournoi_file.close()
        except FileNotFoundError:
            pass

    def newtournament(self, tournoi):
        new_tournoi = Tournoi(tournoi['name'],
                              tournoi['place'],
                              tournoi['start date'],
                              tournoi['end date'],
                              tournoi['desc'],
                              int(float(tournoi['turn number'])),
                              int(float(tournoi['current turn'])),
                              int(float(tournoi['id_tournament'])),
                              tournoi['list turns'],
                              tournoi['list player'],
                              tournoi['list player score']
                              )
        new_pmanager = PlayerManager()
        self.list_tournament.append(new_tournoi)
        list_missing = []
        for player_ine in tournoi['list player']:
            if player_ine:
                if not new_pmanager.exist(player_ine):
                    list_missing.append(player_ine)
        del new_pmanager
        return list_missing

    def tojson(self):
        if self.list_tournament:
            # Write the tournament in json
            with open('./data/tournoi.json', 'w', encoding='utf-8') as tournoi_file:
                list_to_write = []
                for tournament in self.list_tournament:
                    list_to_write.append(tournament.todict())
                json.dump(list_to_write, tournoi_file, indent=4)
                tournoi_file.close()
