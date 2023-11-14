"""Main gui for the tournament tool."""
from __future__ import annotations

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow

from beerpong.gui.login import LoginGUI


class ManagementGUI(QMainWindow):
    """Management gui for the beerpong tool.

    This is the main GUI for the beerpong tool. It lets users enter
    their result and users with management access fix mistakes or
    restart the tournament.
    The main GUI is also responsible for opening (and keeping open) the
    current status gui of the tournament. This is the second screen that
    actually shows the current brackets as well as the current running
    matches.
    """

    def __init__(self) -> None:
        super().__init__()

        self.tournament_name = ""

        self.login_screen: None | LoginGUI = None
        self.brackets_screen = None

        self.setWindowTitle("Beerpong")
        self.setMinimumSize(QSize(1200, 800))
        self.show()

        self.set_management_screen()

    def set_management_screen(self) -> None:
        """Set the management screen.

        The management screen first opens the login screen to select
        the tournament. After the login, the management screen is
        is used for the players to enter their results as well as for
        the management to fix mistakes or restart the tournament.
        """
        self.open_login_screen()

    def open_login_screen(self) -> None:
        """Open the login screen.

        The login screen really is just for selecting the tournament.
        After the user created a new tournament and closes the login
        screen, the brackets screen is opened.
        """

        def transfer_tournament_name(tournament_name: str) -> None:
            self.tournament_name = tournament_name
            self.open_brackets_screen()

        if self.login_screen is None:
            self.login_screen = LoginGUI()
            self.login_screen.create_clicked.connect(transfer_tournament_name)

        self.login_screen.show()

    def open_brackets_screen(self) -> None:
        """Open the brackets screen."""
        # TODO: implement
