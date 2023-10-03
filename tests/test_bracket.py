"""Test the Team class."""

import unittest

from beerpong.logic.bracket import Bracket, Score
from beerpong.logic.team import Team


class TestScore(unittest.TestCase):
    def test_score_correctly_saves_values(self):
        """Test that the score is set correctly."""
        score = Score(10, 5)
        self.assertEqual(score.left, 10)
        self.assertEqual(score.right, 5)

    def test_score_only_accepts_integers(self):
        """Test that the score only accepts integers."""
        with self.assertRaises(TypeError):
            Score(10.5, 5.5)

    def test_score_only_accepts_positiv_integers(self):
        """Test that the score only accepts integers."""
        with self.assertRaises(ValueError):
            Score(-1, 0)


class TestBracket(unittest.TestCase):
    def test_full_bracket(self):
        """Test that the bracket is set correctly."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        bracket = Bracket(team1, team2)
        self.assertEqual(bracket.left, team1)
        self.assertEqual(bracket.right, team2)
        self.assertIsNone(bracket._winner)

    def test_no_empty_bracket(self):
        """Test that the bracket cannot be empty."""
        with self.assertRaises(ValueError):
            Bracket(None, None)

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

    def test_enter_score_to_get_winner_from_left(self):
        """Test that we can enter the score and get the winner."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        bracket = Bracket(team1, team2)
        bracket.set_score(10, 5)
        self.assertEqual(bracket._winner, team1)

    def test_enter_score_to_get_winner_from_right(self):
        """Test that we can enter the score and get the winner."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        bracket = Bracket(team1, team2)
        bracket.set_score(3, 7)
        self.assertEqual(bracket._winner, team2)

    def test_draw_has_no_winner(self):
        """Test that we can enter a draw and get no winner."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        bracket = Bracket(team1, team2)
        bracket.set_score(5, 5)
        self.assertIsNone(bracket.winner)

    def test_score_only_accepts_integers(self):
        """Test that the score only accepts integers."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        bracket = Bracket(team1, team2)
        with self.assertRaises(TypeError):
            bracket.set_score(10.5, 5.5)

    def test_score_only_accepts_positiv_integers(self):
        """Test that the score only accepts integers."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        bracket = Bracket(team1, team2)
        with self.assertRaises(ValueError):
            bracket.set_score(-1, 0)

    def test_manually_setting_score_raises_error(self):
        """Test that we cannot manually set the score."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        bracket = Bracket(team1, team2)
        with self.assertRaises(AttributeError):
            bracket.score = Score(10, 5)

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
        bracket.set_score(10, 5)
        self.assertEqual(bracket.winner, bracket._winner)

    def test_score_property_returns_internal_score(self):
        """Test that the score property returns the internal score."""
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        bracket = Bracket(team1, team2)
        bracket.set_score(10, 5)
        self.assertEqual(bracket.score, bracket._score)
