import warnings

from PyQt6.QtWidgets import QApplication

from beerpong.gui.gui import BeerpongGUI


class Beerpong:
    def __init__(self):
        self.app = QApplication([])
        self.gui = BeerpongGUI()

    def run(self):
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
