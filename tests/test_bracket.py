"""Test the Team class."""

import unittest

from beerpong.logic.bracket import Bracket, Score
from beerpong.logic.team import Team


class TestBracket(unittest.TestCase):
    def test_full_bracket(self):
        """Test that the bracket is set correctly."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        bracket = Bracket(team1, team2)
        self.assertEqual(bracket.left, team1)
        self.assertEqual(bracket.right, team2)
        self.assertIsNone(bracket._winner)

    def test_allow_empty_bracket(self):
        """Test that the bracket can be empty.

        This is crucial because when we create a new tournament, a lot
        of the brackets will in fact be empty as the winners from the
        previous round have not been determined yet.
        """
        bracket = Bracket(None, None)
        self.assertIsNone(bracket.left)
        self.assertIsNone(bracket.right)

    def test_no_same_teams(self):
        """Test that the bracket cannot have the same team twice."""
        team1 = Team("Team 1")
        with self.assertRaises(ValueError):
            Bracket(team1, team1)

    def test_auto_promote_to_winner_from_right(self):
        """Test that if only one team is set, it is automatically
        promoted to winner.
        """
        winner_team = Team("Winner")
        bracket = Bracket(None, winner_team)
        self.assertIsNone(bracket.left)
        self.assertEqual(bracket.right, winner_team)
        self.assertEqual(bracket._winner, winner_team)

    def test_auto_promote_to_winner_from_left(self):
        """Test that if only one team is set, it is automatically
        promoted to winner.
        """
        winner_team = Team("Winner")
        bracket = Bracket(winner_team, None)
        self.assertIsNone(bracket.right)
        self.assertEqual(bracket.left, winner_team)
        self.assertEqual(bracket._winner, winner_team)

    def test_teams_not_valid_type(self):
        """Test that the teams must be Team objects."""
        team = Team("Team")
        with self.assertRaises(TypeError):
            Bracket("left", team)
        with self.assertRaises(TypeError):
            Bracket(team, "right")

    def test_teams_as_brackets(self):
        """Test that the teams can be brackets."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        bracket1 = Bracket(team1, team2)
        bracket2 = Bracket(bracket1, None)
        self.assertIsNone(bracket2.left)  # Still None because bracket1 has no score
        self.assertIsNone(bracket2.right)

    def test_teams_are_none_if_brackets_have_no_winner(self):
        """Test that the teams are None if the brackets have no winner."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        team3 = Team("Team 3")
        team4 = Team("Team 4")
        bracket12 = Bracket(team1, team2)
        bracket34 = Bracket(team3, team4)
        bracket1234 = Bracket(bracket12, bracket34)
        self.assertIsNone(bracket1234.left)
        self.assertIsNone(bracket1234.right)

    def test_teams_as_brackets_propagate_winner_from_left(self):
        """Test that the teams can be brackets."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        bracket1 = Bracket(team1, team2)
        bracket2 = Bracket(bracket1, None)
        bracket1.score = (10, 5)
        self.assertEqual(bracket2.left, team1)
        self.assertIsNone(bracket2.right)

    def test_teams_as_brackets_propagate_winner_from_right(self):
        """Test that the teams can be brackets."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        bracket1 = Bracket(team1, team2)
        bracket2 = Bracket(None, bracket1)
        bracket1.score = (5, 10)
        self.assertEqual(bracket2.right, team2)
        self.assertIsNone(bracket2.left)

    def test_setting_score_as_score_object(self):
        """Test that we can set the score as a Score object."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        bracket = Bracket(team1, team2)
        score = Score(10, 5)
        bracket.score = score
        self.assertEqual(bracket._score, score)

    def test_setting_score_as_tuple(self):
        """Test that we can set the score as a tuple."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        bracket = Bracket(team1, team2)
        score = (10, 5)
        bracket.score = score
        self.assertEqual(bracket._score, Score(*score))

    def test_setting_score_as_invalid_type(self):
        """Test that we cannot set the score as an invalid type."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        bracket = Bracket(team1, team2)
        with self.assertRaises(TypeError):
            bracket.score = "10:5"

    def test_enter_score_to_get_winner_from_left(self):
        """Test that we can enter the score and get the winner."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        bracket = Bracket(team1, team2)
        bracket.score = (10, 5)
        self.assertEqual(bracket._winner, team1)

    def test_enter_score_to_get_winner_from_right(self):
        """Test that we can enter the score and get the winner."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        bracket = Bracket(team1, team2)
        bracket.score = (3, 7)
        self.assertEqual(bracket._winner, team2)

    def test_draw_has_no_winner(self):
        """Test that we can enter a draw and get no winner."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        bracket = Bracket(team1, team2)
        bracket.score = (5, 5)
        self.assertIsNone(bracket.winner)

    def test_winner_with_left_bracket_as_team(self):
        """Test that we can determine the winner of a match when the
        left team is a winner from a previous match.
        """
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        team3 = Team("Team 3")
        bracket12 = Bracket(team1, team2)
        bracket123 = Bracket(bracket12, team3)
        bracket12.score = (10, 5)
        self.assertEqual(bracket12.winner, team1)
        self.assertEqual(bracket123.left, team1)
        self.assertEqual(bracket123.right, team3)
        bracket123.score = (10, 5)
        self.assertEqual(bracket123.winner, team1)

    def test_winner_with_right_bracket_as_team(self):
        """Test that we can determine the winner of a match when the
        right team is a winner from a previous match.
        """
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        team3 = Team("Team 3")
        bracket12 = Bracket(team1, team2)
        bracket123 = Bracket(team3, bracket12)
        bracket12.score = (5, 10)
        self.assertEqual(bracket12.winner, team2)
        self.assertEqual(bracket123.left, team3)
        self.assertEqual(bracket123.right, team2)
        bracket123.score = (5, 10)
        self.assertEqual(bracket123.winner, team2)

    def test_winner_with_two_brackets_as_teams(self):
        """Test that we can determine the winner of a match when both
        teams are winners from previous matches.
        """
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        team3 = Team("Team 3")
        team4 = Team("Team 4")
        bracket12 = Bracket(team1, team2)
        bracket34 = Bracket(team3, team4)
        bracket1234 = Bracket(bracket12, bracket34)
        bracket12.score = (10, 5)
        bracket34.score = (5, 10)
        self.assertEqual(bracket12.winner, team1)
        self.assertEqual(bracket34.winner, team4)
        self.assertEqual(bracket1234.left, team1)
        self.assertEqual(bracket1234.right, team4)
        bracket1234.score = (10, 5)
        self.assertEqual(bracket1234.winner, team1)

    def test_score_only_accepts_integers(self):
        """Test that the score only accepts integers."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        bracket = Bracket(team1, team2)
        with self.assertRaises(TypeError):
            bracket.score = (10.5, 5.5)

    def test_score_only_accepts_positiv_integers(self):
        """Test that the score only accepts integers."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        bracket = Bracket(team1, team2)
        with self.assertRaises(ValueError):
            bracket.score = (-1, 0)

    def test_setting_score_fails_if_left_team_is_none(self):
        """Test that we cannot set the score if the left team is None."""
        team1 = Team("Team 1")
        bracket = Bracket(None, team1)
        with self.assertRaises(ValueError):
            bracket.score = (10, 5)

    def test_setting_score_fails_if_right_team_is_none(self):
        """Test that we cannot set the score if the right team is None."""
        team1 = Team("Team 1")
        bracket = Bracket(team1, None)
        with self.assertRaises(ValueError):
            bracket.score = (10, 5)

    def test_setting_score_fails_if_previous_left_winner_is_none(self):
        """Test that we cannot set the score if the previous winner is
        None.
        """
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        team3 = Team("Team 3")
        bracket12 = Bracket(team1, team2)
        bracket123 = Bracket(bracket12, team3)
        with self.assertRaises(ValueError):
            bracket123.score = (10, 5)

    def test_setting_score_fails_if_previous_right_winner_is_none(self):
        """Test that we cannot set the score if the previous winner is
        None.
        """
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        team3 = Team("Team 3")
        bracket12 = Bracket(team1, team2)
        bracket123 = Bracket(team3, bracket12)
        with self.assertRaises(ValueError):
            bracket123.score = (10, 5)

    def test_manually_setting_winner_raises_error(self):
        """Test that we cannot manually set the winner."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        bracket = Bracket(team1, team2)
        with self.assertRaises(AttributeError):
            bracket.winner = team1

    def test_winner_property_returns_internal_winner(self):
        """Test that the winner property returns the internal winner."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        bracket = Bracket(team1, team2)
        bracket.score = (10, 5)
        self.assertEqual(bracket.winner, bracket._winner)

    def test_score_property_returns_internal_score(self):
        """Test that the score property returns the internal score."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        bracket = Bracket(team1, team2)
        bracket.score = (10, 5)
        self.assertEqual(bracket.score, bracket._score)
