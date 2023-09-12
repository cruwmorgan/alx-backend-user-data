#!/usr/bin/env python3
"""
    Auth module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Bcrypt a password
        Args:
            password: a string

        Return;
            bytes
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ Initialisation """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ New user registration
            Args:
                email: email to check and register
                password: password to hash and register
            Return:
                User object or raises ValueError
        """
        try:
            # search for user in DB
            find_user = self._db.find_user_by(email=email)
            if find_user is not None:
                """ If a user already exist with the passed email, raise a
                ValueError """
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass
        # If not, hash the password with _hash_password
        hashed_password = _hash_password(password)
        # Save the user to the database using self._db
        user = self._db.add_user(email, hashed_password)
        # Return the User object
        return user
