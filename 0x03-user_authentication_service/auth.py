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
            self._db.find_user_by(email=email)
            """ If a user already exist with the passed email, raise a
            ValueError """
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            passwd: str = _hash_password(password)
            user = self._db.add_user(email, passwd)

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """ chcks for valid login
            Args:
                email: email address
                password: password inputed
            Return:
                True or False if user is registered or not
        """
        if email is None or password is None:
            return False

        try:
            user: User = self._db.find_user_by(email=email)
            passwd: bytes = user.hashed_password
            valid: bool = bcrypt.checkpw(password.encode('utf-8'),
                                         passwd)

            return valid
        except NoResultFound:
            return False
