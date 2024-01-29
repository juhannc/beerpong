"""Main gui for the tournament tool."""

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget


class BeerpongGUI(QMainWindow):
    """Main gui for the beerpong tool.

    The main gui contains the management tools needed to run a beerpong
    tournament.
    """

    def __init__(self) -> None:
        super().__init__()

        self.tournament_name = ""

        self.setWindowTitle("Beerpong")
        self.setMinimumSize(QSize(800, 600))
        self.show()

        self.new_tournament_name = QLineEdit(self)
        self.new_tournament_name.setPlaceholderText("My beerpong event")
        self.new_tournament_name.text()
        self.create_tournament_button = QPushButton("Create tournament", self)
        self.create_tournament_button.clicked.connect(self.create_tournament)

        layout = QVBoxLayout()
        layout.addWidget(self.new_tournament_name)
        layout.addWidget(self.create_tournament_button)

        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

    def create_tournament(self) -> None:
        """Create a new tournament."""
        self.tournament_name = self.new_tournament_name.text()
