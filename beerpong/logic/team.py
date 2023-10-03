"""Module to represent a generic team."""
import string
from dataclasses import dataclass, field
from random import SystemRandom

PASSWORD_LENGTH = 4
PASSWORD_VALID_CHARS = string.ascii_lowercase + string.digits


@dataclass
class Team:
    """Class object to represent a generic team."""

    name: str
    _otp: str = field(
        default_factory=str,
        init=False,
        repr=False,
        hash=False,
        compare=False,
    )
    _password_hash: int = field(default_factory=int, init=False)

    def __post_init__(self):
        """Post init steps to ensure the team is valid.

        Check that the team name is not empty and generate a password.
        """
        if not self.name:
            raise ValueError("Team name cannot be empty")
        self._otp = self.__generate_password_string()
        self._password_hash = hash(self._otp)

    def __generate_password_string(self) -> str:
        """Generate a random password for the team.

        The password is a string of random characters of a given length.
        """
        cryptogen = SystemRandom()
        return "".join(cryptogen.choices(PASSWORD_VALID_CHARS, k=PASSWORD_LENGTH))

    def validate_password(self, password: str) -> bool:
        """Validate the password for the team.

        Currently, we only check that the password is equal to the
        generated password. In the future, we could add more checks.

        Also, currently we are only using lower-case letters and digits.
        We could transform the input into lower-case letters and digits
        to make the password case-insensitive.
        """
        return hash(password) == self._password_hash

    @property
    def password(self) -> str:
        """Return the one-time password for the team.

        After the password has been read once, it is deleted."""
        tmp_otp = self._otp
        self._otp = ""
        return tmp_otp

    @password.setter
    def password(self, value: str):
        """Setting the password is not allowed."""
        raise AttributeError("Password cannot be set manually.")
