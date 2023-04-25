from views.playerview import PlayerView
from views.tournamentview import TournamentView
from views.menuview import Menuview
from controllers.tournamentmanager import TournamentManager


class MenuManager:

    def __init__(self):
        self.tournamentmanager = TournamentManager()
        self.tournamentview = TournamentView(self.tournamentmanager)
        self.menuview = Menuview()
        playermanager = self.tournamentmanager.getplayermanager()
        self.playerview = PlayerView(playermanager)
        self.menuview.welcome()
        self.askcommand()

    def askcommand(self):
        while True:
            command = self.menuview.askcommandmenu()
            uncased_command = command.casefold()
            if uncased_command == "tournoi":
                self.tournamentview.askcommandtournament()
            elif uncased_command == "joueur":
                self.playerview.askcommandplayer()
            elif uncased_command == "exit":
                self.menuview.goodbye()
                break
            else:
                print('Commande non comprise\n\n')
