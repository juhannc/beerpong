"""CLI interface for the beerpong tool."""
import warnings

from PyQt6.QtWidgets import QApplication

from beerpong.gui.gui import BeerpongGUI


class Beerpong:
    """Class to run the beerpong tool."""

    def __init__(self):
        self.app = QApplication([])
        self.gui = BeerpongGUI()

    def run(self):
        """Run the beerpong tool."""
        self.gui.show()
        self.app.exec()


def beerpong() -> None:
    """Run the beerpong tool."""
    ponger = Beerpong()
    ponger.run()


if __name__ == "__main__":
    warnings.warn(
        RuntimeWarning("Please use the cli tools to run beerpong."),
        stacklevel=2,
    )
    beerpong()  # pylint: disable=no-value-for-parameter
