from controllers.tournamentmanager import TournamentManager
from controllers.myappexception import MyAppBadPlayerCount, MyAppDontPlayThisMatch, MyAppAlreadyInException


class TournamentView:
    def __init__(self, tournamentmanager: TournamentManager):
        self.tournamentmanager = tournamentmanager
        self.turnmanager = tournamentmanager.turnmanager
        self.matchmanager = tournamentmanager.matchmanager
        self.playermanager = tournamentmanager.playermanager

    def askcommandtournament(self):
        while True:
            print('\n'
                  'Quel action souhaitez vous effectuer?\n'
                  'Voir la liste des tournois | Liste\n'
                  'Voir un tournoi | Tournoi tournoi_id\n'
                  'Créer un nouveau tournoi | Nouveau\n'
                  'Retour Menu | Menu')
            choice = input().casefold()
            first_word = choice.split()
            if choice == "liste":
                self.viewlisttournament()
            elif first_word and first_word[0] == "tournoi" and len(first_word) == 2:
                try:
                    self.viewtournament(int(float(first_word[1])))
                except ValueError:
                    print(f' \'{first_word[0]}\' n\'est pas un nombre')
            elif first_word and first_word[0] == "nouveau":
                self.viewnewtournament()
            elif choice == "menu":
                break
            else:
                print('Commande non comprise')

    def viewlisttournament(self):
        liste_tournoi = self.tournamentmanager.getlisttournament()
        if liste_tournoi:
            print("\n"
                  " ID_tournoi  | Nom")
            for tournoi in liste_tournoi:
                id_tournoi = tournoi['id_tournament']
                name = tournoi['name']
                print(f'    {id_tournoi}    | {name}')
        else:
            print('\n Aucun tournoi connu')

    def viewtournament(self, tournoi_id):
        while True:
            tournoi = self.tournamentmanager.getinfotournament(tournoi_id)
            if not tournoi:
                print('\n'
                      'ID tournoi non trouvé')
                break
            id_tournoi = tournoi['id_tournament']
            name = tournoi['name']
            place = tournoi['place']
            start = tournoi['start_date']
            end = tournoi['end_date']
            turnmax = tournoi['turn_number']
            turncurrent = tournoi['current_turn']
            desc = tournoi['desc']
            print(f'\n'
                  f'ID: {id_tournoi}\n'
                  f'Nom: {name}\n'
                  f'Place: {place}\n'
                  f'Debut: {start}')
            if end != '':
                print(f'Fin: {end}')
            print(f'Nombre de tours: {turnmax}\n'
                  f'Tour en cours: {turncurrent}\n'
                  f'Description: {desc}\n')
            print('Quel action souhaitez vous effectuer?\n'
                  'Voir la liste des joueurs inscrits | Joueurs\n'
                  'Voir liste des tours et des matchs | tour-match')
            if end == '':
                # Check if all matchs of the current turn are done
                allmatchdone = self.tournamentmanager.allmatchdone(tournoi_id)
                islastturn = self.tournamentmanager.islastturn(tournoi_id)
                if allmatchdone:
                    if not islastturn:
                        print('Continuer le tournoi | Continue')
                    else:
                        print('Clore le tournoi | Continue')
                else:
                    print('Certains matchs sont toujours en cours !!')
            print('Retour à la liste des tournois | Retour')
            choice = input().casefold()
            if choice == "joueurs":
                self.listplayertournament(tournoi_id)
            elif choice == "tour-match":
                self.viewturnmatch(tournoi_id)
            elif choice == "continue":
                if end == '':
                    try:
                        if self.tournamentmanager.advanceturn(tournoi_id):
                            print('Tournoi avancé !')
                        else:
                            print('Impossible de continuer le tournoi , vérifier que les matchs sont finis')
                    except MyAppBadPlayerCount:
                        print('Impossible de continuer le tournoi, si le nombre de joueur est impaire ou 0')
                else:
                    print('Impossible de continuer un tournoi clos')
            elif choice == "retour":
                break
            else:
                print('Commande non comprise\n\n')

    def listplayertournament(self, tournoi_id):
        while True:
            list_player_name = self.tournamentmanager.getlistplayer(tournoi_id)
            if list_player_name:
                print('\n'
                      '   INE   | Nom     | Score tour fini ')
                list_player_name.sort(key=lambda a: a[1])
                list_score = self.tournamentmanager.getlistscore(tournoi_id)
                for player in list_player_name:
                    if list_score:
                        for score in list_score:
                            if score[0] == player[0]:
                                print(f'{player[0]}  {player[1]} : {score[1]}')
                                break
                    else:
                        print(f'{player[0]}  {player[1]}')

                print('\n')
            else:
                print('Aucun joueur inscrit\n')
            # Check if the tournament is already started
            can_add_player = False
            if not self.tournamentmanager.getlistturn(tournoi_id):
                can_add_player = True
                print('Ajouter un joueur par son INE| Ajouter joueur_ine')
            print('Retour au tournoi | Retour')
            choice = input().casefold()
            first_word = choice.split()
            if first_word and len(first_word) == 2 and first_word[0] == "ajouter" and can_add_player:
                try:
                    self.tournamentmanager.addplayer(tournoi_id, first_word[1].upper())
                    print(f'{first_word[1].upper()} inscrit à ce tournoi')
                except MyAppAlreadyInException:
                    print(f'{first_word[1].upper()} déjà inscrit à ce tournoi')
            elif choice == "retour":
                break
            else:
                print('Commande non comprise')

    def viewturnmatch(self, tournoi_id):
        while True:
            list_turns = self.tournamentmanager.getlistturn(tournoi_id)
            if list_turns:
                all_done = True
                for turn_id in list_turns:
                    turn = self.turnmanager.getinfoturn(turn_id)
                    id_turn = turn['id_turn']
                    name = turn['name']
                    start = turn['start_time']
                    end = turn['end_time']
                    print(f'\nNom: {name}\n'
                          f'ID Tour: {id_turn}\n'
                          f'Debut: {start}')
                    if end is not None:
                        print(f'Fin: {end}')
                    list_matchs = turn['list_matchs']
                    print('Liste des Matchs')
                    for match_id in list_matchs:
                        match = self.matchmanager.getmatchinfo(match_id)
                        id_match = match['id_match']
                        matched_player_score = self.matchmanager.readablescore(match['matched_player_score'])
                        print(f'ID Match: {id_match}\n'
                              f'Score Initial: {matched_player_score}')
                        if match['end_score'] is None:
                            all_done = False
                        else:
                            end_score = self.matchmanager.readablescore(match['end_score'])
                            winner = self.matchmanager.getwinner(match['matched_player_score'], match['end_score'])
                            print(f'Score Final: {end_score}\n'
                                  f'Vainqueur: {winner}')
                print('Quel action souhaitez vous effectuer?')
                if not all_done:
                    print('Voir un match | Match match_id')
            else:
                print('\nLe tournoi n\'est pas commencé')
            print('Retour au tournoi | Retour')
            choice = input().casefold()
            first_word = choice.split()
            if first_word and first_word[0] == "match" and len(first_word) == 2:
                try:
                    self.viewmatch(int(float(first_word[1])))
                except ValueError:
                    print(f' \'{first_word[0]}\' n\'est pas un nombre')
            elif choice == "retour":
                break
            else:
                print('Commande non comprise\n\n')

    def viewmatch(self, match_id):
        while True:
            match = self.matchmanager.getmatchinfo(match_id)
            if match:
                game_over = False
                id_match = match['id_match']
                matched_player_score = self.matchmanager.readablescore(match['matched_player_score'])
                print(f'ID Match: {id_match}\n'
                      f'Score Initial: {matched_player_score}')
                if match['end_score'] is not None:
                    game_over = True
                    end_score = self.matchmanager.readablescore(match['end_score'])
                    winner = self.matchmanager.getwinner(match['matched_player_score'], match['end_score'])
                    print(f'Score Final: {end_score}\n'
                          f'Vainqueur: {winner}')

                print('Quel action souhaitez vous effectuer?')
                if not game_over:
                    print('Annoncer un vainqueur | Win joueur_id')
                    print('Annoncer une match nul | Draw')
                print('Retour au tournoi | Retour')
                choice = input().casefold()
                first_word = choice.split()
                if first_word and first_word[0] == "win" and len(first_word) == 2:
                    try:
                        self.matchmanager.win(match_id, first_word[1].upper())
                    except MyAppDontPlayThisMatch:
                        print(f'{first_word[1].upper()} ne joue pas dans ce match')
                elif choice == "draw":
                    self.matchmanager.draw(match_id)
                elif choice == "retour":
                    break
                else:
                    print('Commande non comprise\n\n')
            else:
                print('Aucun match trouvé avec cette ID')
                input("Appuyer sur \'Entrée\' pour revenir à la liste des matchs...")
                break

    def viewnewtournament(self):
        while True:
            name = input('Nom: ')
            if self.tournamentmanager.tournamentexist(name):
                place = input('Place: ')
                start_date = input('Date de début \'AAAA-MM-JJ\': ')
                desc = input('Description: ')
                turn_max = input('Nombre de tour: ')
                new_tournament = {"name": name,
                                  "place": place,
                                  "start_date": start_date,
                                  "desc": desc,
                                  "turn_number": turn_max,
                                  }
                id_tournament = self.tournamentmanager.addtournament(new_tournament)
                if id_tournament:
                    print(f'Le tournoi {name} a été créé avec l\'ID: {id_tournament}')
                    break
                else:
                    print('Le tournoi n\'as pas été créé')
                    break
            else:
                print('Un tournoi porte déjà ce nom')
                break
