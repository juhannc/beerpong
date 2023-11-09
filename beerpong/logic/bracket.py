"""Class to represent a single bracket in the tournament."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from annotated_types import Ge
from typing_extensions import (  # TODO: Use typing.Annotated when dropping 3.8 support
    Annotated,
)

from beerpong.logic.score import Score
from beerpong.logic.team import Team


@dataclass
class Bracket:
    """Class to represent a single bracket in the tournament.

    A bracket always has a left and right element, similar to a binary
    tree. Each element can be either a team, another bracket, or None.
    If the element is another bracket, the winner of that bracket is
    used as the team for this bracket. If the element is None, the
    other element's team is automatically the winner of this bracket.

    Each bracket currently only has one score property, which is the
    score of the bracket. This score is used to determine the winner
    of the bracket. If the score is not set, the winner is None. Same
    goes if the score is set to a tie.

    :param left: The left element (team) of the bracket.
    :type left: Team | Bracket | None
    :param right: The right element (team) of the bracket.
    :type right: Team | Bracket | None
    """

    left: Team | Bracket | None
    right: Team | Bracket | None
    _score: Score | None = field(default=None, init=False)
    _winner: Team | None = field(default=None, init=False)

    def __post_init__(self):
        """Post init steps to ensure the bracket is valid.

        Check that the left and right teams are not the same.
        """
        if self.left == self.right and self.left is not None and self.right is not None:
            raise ValueError("Left and right teams cannot be the same")

        if not isinstance(self.left, (Team, Bracket)) and self.left is not None:
            raise TypeError("Left team must be a Team or Bracket object")
        if not isinstance(self.right, (Team, Bracket)) and self.right is not None:
            raise TypeError("Right team must be a Team or Bracket object")

        # If we only have one team, that team is the winner by default
        if self.left is None and self.right is not None:
            self._winner = (
                self.right if isinstance(self.right, Team) else self.right.winner
            )
        elif self.left is not None and self.right is None:
            self._winner = (
                self.left if isinstance(self.left, Team) else self.left.winner
            )

    def __getattribute__(self, __name: str) -> Any:
        """Overwrite the default __getattribute__ method.

        The default __getattribute__ method is overwritten to return
        the winner of the bracket if the value of the left or right
        attribute is a bracket.

        :param __name: The name of the attribute to get.
        :type __name: str

        :return: The value of the attribute.
        """
        if __name == "left" and isinstance(super().__getattribute__(__name), Bracket):
            return super().__getattribute__(__name).winner
        if __name == "right" and isinstance(super().__getattribute__(__name), Bracket):
            return super().__getattribute__(__name).winner
        return super().__getattribute__(__name)

    @property
    def score(self) -> Score | None:
        """Return the score for the bracket.

        :return: The score of the bracket.
        """
        return self._score

    @score.setter
    def score(
        self, value: Score | tuple[Annotated[int, Ge(0)], Annotated[int, Ge(0)]]
    ) -> None:
        """Set the score for the bracket.

        The score of a bracket determines the winner of said bracket.
        The score can either be of type Score of a tuple of two
        integers.

        :param value: The score to set.
        :type value: Score | tuple[int, int]

        :raises TypeError: If the score is not a Score object or a tuple.
        :raises ValueError: If the left and right teams are not set.
        """
        if isinstance(value, Score):
            self._score = value
        elif isinstance(value, tuple):
            self._score = Score(*value)
        else:
            raise TypeError("Score must be a Score object or a tuple")
        if self.left is None or self.right is None:
            raise ValueError(
                "Left and right teams must be set before setting the score"
            )
        if self._score.left > self._score.right:
            self._winner = (
                self.left if isinstance(self.left, Team) else self.left.winner
            )
        elif self._score.left < self._score.right:
            self._winner = (
                self.right if isinstance(self.right, Team) else self.right.winner
            )
        else:
            self._winner = None

    @property
    def winner(self) -> Team | None:
        """Return the winner of the bracket.

        :return: The winner of the bracket.
        """
        return self._winner

    @winner.setter
    def winner(self, value: Team) -> None:
        """Setting the winner is not allowed.

        :param value: The winner to set (not allowed).
        :type value: Team
        """
        raise AttributeError(
            "Winner cannot be set manually. Please set the score instead."
        )
