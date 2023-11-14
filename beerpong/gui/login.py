"""Main gui for the tournament tool."""
from pathlib import Path

from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

BACKGROUND_IMAGE = Path(
    Path(__file__).parent.parent.parent, "assets", "playingfield.jpeg"
)


class LoginGUI(QMainWindow):
    """Login gui for the beerpong tool.

    The login gui creates the login screen and lets users create a new
    tournament.
    """

    create_clicked = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()

        self.tournament_name = ""

        self.setWindowTitle("New Beerpong")
        self.setMinimumSize(QSize(1200, 600))
        self.show()

        self.set_login_screen()

    def set_login_screen(self) -> None:
        """Set the login screen."""
        self.new_tournament_label = QLabel(
            "Create a new tournament or choose an existing one", self
        )
        font = self.new_tournament_label.font()
        font.setBold(True)
        font.setPointSize(24)
        self.new_tournament_label.setFont(font)
        self.new_tournament_label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )

        self.login_image = QLabel(self)
        self.login_image.setPixmap(QPixmap(str(BACKGROUND_IMAGE)))
        self.login_image.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )

        self.create_tournament_button = QPushButton("Create tournament", self)
        self.create_tournament_button.clicked.connect(self.create_tournament)

        self.new_tournament_name = QLineEdit(self)
        self.new_tournament_name.setPlaceholderText("My beerpong event")
        self.new_tournament_name.returnPressed.connect(
            self.create_tournament_button.click
        )

        self.previous_tournaments = QComboBox(self)
        self.previous_tournaments.addItems(
            ["Previous tournament 1", "Previous tournament 2"]
        )  # TODO: replace with data from backend once implemented

        main_layout = QVBoxLayout()
        name_layout = QHBoxLayout()

        main_layout.addWidget(self.new_tournament_label)

        main_layout.addWidget(self.login_image)

        name_layout.addWidget(self.new_tournament_name)
        name_layout.addWidget(self.previous_tournaments)

        main_layout.addLayout(name_layout)
        main_layout.addWidget(self.create_tournament_button)

        container = QWidget()
        container.setLayout(main_layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

    def create_tournament(self) -> None:
        """Create a new tournament.

        First, read the name of the tournament from the text field or,
        if none is given, from the combo box. Then emit the signal to
        exchange the tournament name with the main gui and close the
        login screen.
        """
        label_text = self.new_tournament_name.text()
        combo_test = self.previous_tournaments.currentText()
        self.tournament_name = label_text if label_text != "" else combo_test

        self.create_clicked.emit(self.tournament_name)

        self.close()
