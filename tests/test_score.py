"""Test the Score class."""

import unittest

from beerpong.logic.score import Score


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
