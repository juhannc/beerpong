"""Class to represent the score of a single bracket in the tournament."""

from dataclasses import dataclass


@dataclass
class Score:
    left: int
    right: int

    def __post_init__(self):
        """Post init steps to ensure the score is valid.

        Check that the score is not negative.
        """
        if self.left < 0 or self.right < 0:
            raise ValueError("Score cannot be negative")
        if not isinstance(self.left, int) or not isinstance(self.right, int):
            raise TypeError("Score must be an integer")
