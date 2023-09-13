#!/usr/bin/env python3
"""
    Auth module
"""
import bcrypt
from db import DB
from typing import Union
from uuid import uuid4
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


def _generate_uuid() -> str:
    """Generates a uuid.

    Returns:
        str: string representation of a new UUID.
    """
    return str(uuid4())


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

    def create_session(self, email: str) -> str:
        """ craete a user session
            Args:
                email: email of user
            Return:
                Session ID of user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            # Return None if no user is found with given email
            return None
        # If user is None, return None
        if user is None:
            return None
        # Generate a new UUID and store it in the db as the user’s session_id
        session_id: str = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        # Return the session ID.
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ Get a User from session id
            Args:
                session_id: Id session
            Return:
                User or None
        """
        # If the session ID is None or no user is found, return None
        if session_id is None:
            return None
        try:
            # Attempt to retrieve the user object corresponding to the session
            # ID from the database
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            # If no user object is found, return None
            return None
        # Otherwise return the corresponding user.
        return user
