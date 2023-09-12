#!/usr/bin/env python3
"""
    DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
            Create a new user

            Args:
                email: String email to add
                hashed_password: Password to add

            Return:
                User ID created
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """Get user from DB
            Args:
                kwargs: Arbitrary keyword arguments
            Return:
                first row found in the users table as filtered by the
                method’s input arguments
        """
        if not kwargs:
            raise InvalidRequestError

        cols_keys = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in cols_keys:
                raise InvalidRequestError

        users = self._session.query(User).filter_by(**kwargs).first()

        if users is None:
            raise NoResultFound

        return users
