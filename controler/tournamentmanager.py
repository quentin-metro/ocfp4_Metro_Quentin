import json
from modele.tournoi import Tournoi
from controler.playermanager import PlayerManager


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
                              tournoi['list player'],
                              tournoi['list player score'],
                              tournoi['desc'],
                              tournoi['list turns'],
                              int(tournoi['current turn']),
                              int(tournoi['turn number']),
                              int(tournoi['id_tournament'])
                              )
        new_pmanager = PlayerManager()
        self.list_tournament.append(new_tournoi)
        list_missing = []
        for player_ine in tournoi['list player']:
            if player_ine:
                if new_pmanager.exist(player_ine):
                    list_missing.append(player_ine)
        del new_pmanager
        return list_missing

    def tojson(self):
        # Write the tournament in json
        with open('./data/tournoi.json', 'w', encoding='utf-8') as tournoi_file:
            list_to_write = []
            for tournament in self.list_tournament:
                list_to_write.append(tournament.todir())
            json.dump(list_to_write, tournoi_file, indent=4)
            tournoi_file.close()
