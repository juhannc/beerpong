"""Class to represent a single bracket in the tournament."""
from __future__ import annotations

from dataclasses import dataclass, field

from beerpong.logic.score import Score
from beerpong.logic.team import Team


@dataclass
class Bracket:
    left: Team | None
    right: Team | None
    _score: Score | None = field(default=None, init=False)
    _winner: Team | None = field(default=None, init=False)

    def __post_init__(self):
        """Post init steps to ensure the bracket is valid.

        Check that the left and right teams are not the same.
        """
        if self.left is None and self.right is None:
            raise ValueError("Left and right teams cannot both be None")
        if self.left == self.right:
            raise ValueError("Left and right teams cannot be the same")

        # If we only have one team, that team is the winner by default
        if self.left is None and self.right is not None:
            self._winner = self.right
        elif self.left is not None and self.right is None:
            self._winner = self.left

    def set_score(self, left: int, right: int):
        """Set the score for the bracket."""
        self._score = Score(left, right)
        if left > right:
            self._winner = self.left
        elif left < right:
            self._winner = self.right
        else:
            self._winner = None

    @property
    def score(self) -> Score | None:
        """Return the score for the bracket."""
        return self._score

    @score.setter
    def score(self, value: Score):
        """Setting the score is not allowed."""
        raise AttributeError(
            "Score cannot be set manually. Please use set_score() instead."
        )

    @property
    def winner(self) -> Team | None:
        """Return the winner of the bracket."""
        return self._winner

    @winner.setter
    def winner(self, value: Team):
        """Setting the winner is not allowed."""
        raise AttributeError(
            "Winner cannot be set manually. Please use set_score() instead."
        )
