from controllers.tournamentmanager import TournamentManager


class TournamentView:
    def __init__(self, tournamentmanager: TournamentManager):
        self.tournamentmanager = tournamentmanager
        self.turnmanager = tournamentmanager.turnmanager
        self.matchmanager = tournamentmanager.matchmanager

    @staticmethod
    def askcommandtournament():
        print(f'Quel action souhaitez vous effectuer?\n'
              f'Voir la liste des tournois | Liste\n'
              f'Voir un tournoi | Tournoi tournoi_id\n'
              f'Retour Menu | Menu')
        return input()

    def viewlisttournament(self):
        liste_tournoi = self.tournamentmanager.getlisttournament()
        print(" ID_tournoi  | Nom")
        for tournoi in liste_tournoi:
            id_tournoi = tournoi['id_tournament']
            name = tournoi['name']
            print(f'{id_tournoi} | {name}\n')
        self.askcommandtournament()

    def viewtournament(self, tournoi_id):
        tournoi = self.tournamentmanager.getinfotournament(tournoi_id)
        id_tournoi = tournoi['id_tournament']
        name = tournoi['name']
        place = tournoi['place']
        start = tournoi['start_date']
        end = tournoi['end_date']
        turnmax = tournoi['turn_number']
        turncurrent = tournoi['current_turn']
        desc = tournoi['desc']
        print(f'ID: {id_tournoi}\n')
        print(f'Nom: {name}\n')
        print(f'Place: {place}\n')
        print(f'Debut: {start}\n')
        if end:
            print(f'Fin: {end}\n')
        print(f'Nombre de tours: {turnmax}\n')
        print(f'Tour en cours: {turncurrent}\n')
        print(f'Description: {desc}\n\n\n')
        print(f'Quel action souhaitez vous effectuer?\n'
              f'Voir la liste des joueurs inscrits | Joueurs\n'
              f'Ajouter un joueur par son INE| Ajouter joueur_ine\n'
              f'Voir liste des tours et des matchs | tour-match\n'
              f'Retour à la liste des tournois | Retour')
        return input()

    def listplayertournament(self, tournoi_id):
        print("   INE   | Nom")
        list_player_name = self.tournamentmanager.getlistplayer(tournoi_id)
        list_player_name.sort(key=lambda a: a[1])
        for player in list_player_name:
            print(f'{player[0]}  {player[1]}')
        print(f'\nRetour au tournoi | Retour')

    def viewturnmatch(self, tournoi_id):
        list_turns = self.tournamentmanager.getlistturn(tournoi_id)
        for turn_id in list_turns:
            turn = self.turnmanager.getinfoturn(turn_id)
            id_turn = turn['id_tournament']
            name = turn['name']
            start = turn['start_date']
            end = turn['end_date']
            print(f'Nom: {name}\n')
            print(f'\fID Tour: {id_turn}\n')
            print(f'\fDebut: {start}\n')
            if end != "":
                print(f'\fFin: {end}\n')
            list_matchs = turn['list_matchs']
            print(f'\fListe des Matchs')
            for match_id in list_matchs:
                match = self.matchmanager.getmatchinfo(match_id)
                id_match = match['id_match']
                matched_player_score = self.matchmanager.readablescore(match['matched_player_score'])
                end_score = self.matchmanager.readablescore(match['end_score'])
                print(f'\f\fID Match: {id_match}\n')
                print(f'\f\fScore Initial: {matched_player_score}\n')
                if end_score != "":
                    print(f'\f\fScore Final: {end_score}\n')
                    winner = self.matchmanager.getwinner(matched_player_score, end_score)
                    print(f'\f\fVainqueur: {winner}')
                # print the winner , matchmanager.getwinner
        print(f'Quel action souhaitez vous effectuer?\n'
              f'Continuer le tournoi | Continue\n'
              f'Retour au tournoi | Retour')
        return input()
