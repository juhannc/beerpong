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
        if (
            self.left is None
            and not isinstance(self.left, Bracket)
            and self.right is not None
        ):
            self._winner = (
                self.right if isinstance(self.right, Team) else self.right.winner
            )
        elif (
            self.left is not None
            and self.right is None
            and not isinstance(self.right, Bracket)
        ):
            self._winner = (
                self.left if isinstance(self.left, Team) else self.left.winner
            )

        # If one of the teams is an empty bracket, the other team is the winner
        if (
            isinstance(self.left, Bracket)
            and self.left.is_empty
            and self.right is not None
        ):
            self._winner = (
                self.right if isinstance(self.right, Team) else self.right.winner
            )
        elif (
            isinstance(self.right, Bracket)
            and self.right.is_empty
            and self.left is not None
        ):
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
        if (
            __name in ("left", "right")
            and isinstance(super().__getattribute__(__name), Bracket)
            and isinstance(super().__getattribute__(__name).winner, Team)
        ):
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
        if not self.is_playable:
            raise RuntimeError("The Bracket is not playable")
        if isinstance(value, Score):
            self._score = value
        elif isinstance(value, tuple):
            self._score = Score(*value)
        else:
            raise TypeError("Score must be a Score object or a tuple")
        # Type checkers do not know that the is_playable check ensures that
        # the left and right teams are of type Team.
        self.left: Team
        self.right: Team
        if self._score.left > self._score.right:
            self._winner = self.left  # type: ignore
        elif self._score.left < self._score.right:
            self._winner = self.right  # type: ignore
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

    @property
    def is_playable(self) -> bool:
        """Return whether the bracket is playable.

        A bracket is playable if both the left and right teams are set
        and no score has been set (aka the winner is not yet
        determined).

        :return: Whether the bracket is playable.
        """
        return (
            isinstance(self.left, Team)
            and isinstance(self.right, Team)
            and self.score is None
        )

    @property
    def is_played(self) -> bool:
        """Return whether the bracket is played.

        A bracket is played if we have a winner of type Team.

        :return: Whether the bracket is played.
        """
        if isinstance(self.winner, Team):
            return True
        if self.left is None and self.right is None:
            return True
        return False

    @property
    def is_empty(self) -> bool:
        """Return whether the bracket is empty.

        A bracket is empty if both the left and right teams are None.

        :return: Whether the bracket is empty.
        """
        return self.left is None and self.right is None
