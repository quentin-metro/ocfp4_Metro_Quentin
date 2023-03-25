from controllers.tournamentmanager import TournamentManager
from controllers.myappexception import MyAppBadPlayerCount


class TournamentView:
    def __init__(self, tournamentmanager: TournamentManager):
        self.tournamentmanager = tournamentmanager
        self.turnmanager = tournamentmanager.turnmanager
        self.matchmanager = tournamentmanager.matchmanager
        self.playermanager = tournamentmanager.playermanager

    def askcommandtournament(self):
        while True:
            print(f'Quel action souhaitez vous effectuer?\n'
                  f'Voir la liste des tournois | Liste\n'
                  f'Voir un tournoi | Tournoi tournoi_id\n'
                  f'Créer un nouveau tournoi | Nouveau\n'
                  f'Retour Menu | Menu')
            choice = input().casefold()
            first_word = choice.split()
            if choice == "liste":
                self.viewlisttournament()
            elif first_word[0] == "tournoi":
                self.viewtournament(first_word[1])
            elif first_word[0] == "nouveau":
                self.viewnewtournament()
            elif choice == "menu":
                break
            else:
                print(f'Commande non comprise\n\n')

    def viewlisttournament(self):
        liste_tournoi = self.tournamentmanager.getlisttournament()
        print(" ID_tournoi  | Nom")
        for tournoi in liste_tournoi:
            id_tournoi = tournoi['id_tournament']
            name = tournoi['name']
            print(f'{id_tournoi} | {name}\n')

    def viewtournament(self, tournoi_id):
        while True:
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
            if end != "":
                print(f'Fin: {end}\n')
            print(f'Nombre de tours: {turnmax}\n')
            print(f'Tour en cours: {turncurrent}\n')
            print(f'Description: {desc}\n\n\n')
            print(f'Quel action souhaitez vous effectuer?\n'
                  f'Voir la liste des joueurs inscrits | Joueurs\n'
                  f'Voir liste des tours et des matchs | tour-match\n')
            if end == "":
                # Check if all matchs of the current turn are done
                allmatchdone = self.tournamentmanager.allmatchdone
                islastturn = self.tournamentmanager.islastturn(tournoi_id)
                if allmatchdone or islastturn:
                    print(f'Tous les matchs et les tours ne sont pas fini')
                else:
                    print(f'Continuer le tournoi | Continue')
            print(f'Retour à la liste des tournois | Retour')
            choice = input().casefold()
            if choice == "joueurs":
                self.listplayertournament(tournoi_id)
            elif choice == "tour-match":
                self.viewturnmatch(tournoi_id)
            elif choice == "continue":
                if end != "":
                    try:
                        self.tournamentmanager.advanceturn(tournoi_id)
                    except MyAppBadPlayerCount:
                        print(f'Impossible de continuer le tournoi, si le nombre de joueur est impaire ou 0')
                else:
                    print(f'Impossible de continuer un tournoi clos')
            elif choice == "retour":
                break
            else:
                print(f'Commande non comprise\n\n')

    def listplayertournament(self, tournoi_id):
        while True:
            print("   INE   | Nom")
            list_player_name = self.tournamentmanager.getlistplayer(tournoi_id)
            list_player_name.sort(key=lambda a: a[1])
            for player in list_player_name:
                print(f'{player[0]}  {player[1]}')
            print(f'\n')
            # Check if the tournament is already started
            can_add_player = False
            if self.tournamentmanager.getlistturn(tournoi_id) == "":
                can_add_player = True
                print(f'Ajouter un joueur par son INE| Ajouter joueur_ine')
            print(f'Retour au tournoi | Retour')
            choice = input().casefold()
            first_word = choice.split()
            if first_word[0] == "liste" and can_add_player:
                self.tournamentmanager.addplayer(tournoi_id, first_word[1])
            elif choice == "retour":
                break
            else:
                print(f'Commande non comprise\n\n')

    def viewturnmatch(self, tournoi_id):
        while True:
            list_turns = self.tournamentmanager.getlistturn(tournoi_id)
            all_done = True
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
                    if end_score == "":
                        all_done = False
                    else:
                        print(f'\f\fScore Final: {end_score}\n')
                        winner = self.matchmanager.getwinner(matched_player_score, end_score)
                        print(f'\f\fVainqueur: {winner}')
            print(f'Quel action souhaitez vous effectuer?')
            if not all_done:
                print(f'Mettre à jour un match | Match match_id')
            print(f'Retour au tournoi | Retour')
            choice = input().casefold()
            first_word = choice.split()
            if first_word[0] == "match":
                self.viewmatch(first_word[1])
                self.tournamentmanager.updatescore(tournoi_id, first_word[1])
            elif choice == "retour":
                break
            else:
                print(f'Commande non comprise\n\n')

    def viewmatch(self, match_id):
        while True:
            match = self.matchmanager.getmatchinfo(match_id)
            if match:
                game_over = False
                id_match = match['id_match']
                matched_player_score = self.matchmanager.readablescore(match['matched_player_score'])
                end_score = self.matchmanager.readablescore(match['end_score'])
                print(f'\f\fID Match: {id_match}\n')
                print(f'\f\fScore Initial: {matched_player_score}\n')
                if end_score != "":
                    game_over = True
                    print(f'\f\fScore Final: {end_score}\n')
                    winner = self.matchmanager.getwinner(matched_player_score, end_score)
                    print(f'\f\fVainqueur: {winner}')

                print(f'Quel action souhaitez vous effectuer?')
                if not game_over:
                    print(f'Annoncer un vainqueur | Win joueur_id')
                    print(f'Annoncer une match nul | Draw')
                print(f'Retour au tournoi | Retour')
                choice = input().casefold()
                first_word = choice.split()
                if first_word[0] == "Win":
                    self.matchmanager.win(match_id, first_word[1])
                elif choice == "draw":
                    self.matchmanager.draw(match_id)
                elif choice == "retour":
                    break
                else:
                    print(f'Commande non comprise\n\n')
            else:
                print(f'Aucun match trouvé avec cette ID')
                input("Appuyer sur \'Entrée\' pour revenir à la liste des matchs...")
                break

    def viewnewtournament(self):
        while True:
            name = input('Nom: ')
            place = input('Place: ')
            start_date = input('Date de début \'AAAA-MM-JJ\': ')
            desc = input('Description: ')
            turn_max = input('Maximum Turn: ')
            new_tournament = {"name": name,
                              "place": place,
                              "start_date": start_date,
                              "desc": desc,
                              "turn_number": turn_max,
                              }
            id_tournament = self.tournamentmanager.createtournament(new_tournament)
            if id_tournament:
                print(f'Le tournoi {name} a été créé avec l\'ID: {id_tournament}')
                break
            else:
                print(f'Le tournoi n\'as pas été créé')
