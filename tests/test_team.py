"""Test the Team class."""

import unittest
from unittest.mock import patch

from beerpong.logic.team import PASSWORD_LENGTH, PASSWORD_VALID_CHARS, Team

PASSWORD_TEST_LENGTH = 10_000


class TestTeam(unittest.TestCase):
    def test_team_name(self):
        """Test that the team name is set correctly."""
        team = Team("Team 1")
        self.assertEqual(team.name, "Team 1")

    def test_team_name_cannot_be_empty(self):
        """Test that the team name cannot be empty."""
        with self.assertRaises(ValueError):
            Team("")

    def test_team_password_length(self):
        """Test that the team password length is set correctly."""
        team = Team("Team 1")
        self.assertEqual(len(team.password), PASSWORD_LENGTH)

    @patch("beerpong.logic.team.PASSWORD_LENGTH", PASSWORD_TEST_LENGTH)
    def test_team_password_valid_chars(self):
        """Test that the team password contains only valid characters.

        We increased the password length to PASSWORD_TEST_LENGTH to
        ensure more of the random characters are tested.
        """
        team = Team("t")
        password = team.password
        self.assertEqual(len(password), PASSWORD_TEST_LENGTH)
        self.assertTrue(set(password).issubset(PASSWORD_VALID_CHARS))

    @patch("beerpong.logic.team.PASSWORD_LENGTH", PASSWORD_TEST_LENGTH)
    def test_team_password_is_random(self):
        """Test that the team password is random.

        We increased the password length to PASSWORD_TEST_LENGTH to
        reduce the probability of a false positive.
        """
        team1 = Team("Team 1")
        team2 = Team("Team 2")
        self.assertNotEqual(team1.password, team2.password)

    def test_team_name_and_password_in_repr_str(self):
        """Test that the team name and password are in the string
        representation of the object.
        """
        team = Team("Team 1")

        self.assertIn(team.name, repr(team))
        self.assertIn(str(team._password_hash), repr(team))

        self.assertIn(team.name, str(team))
        self.assertIn(str(team._password_hash), str(team))

    def test_password_validation(self):
        """Test that the password validation works."""
        team = Team("Team 1")
        self.assertTrue(team.validate_password(team.password))
        self.assertFalse(team.validate_password("wrong_password"))

    def test_password_is_one_time_readable(self):
        """Test that the password is only readable once."""
        team = Team("Team 1")
        password = team.password
        self.assertNotEqual(password, team.password)

    def test_password_cannot_be_set_manually(self):
        """Test that the password cannot be set manually."""
        team = Team("Team 1")
        with self.assertRaises(AttributeError):
            team.password = (
                "new_password"  # nosec - wrongly triggers hardcoded password
            )
