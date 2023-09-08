#!/usr/bin/env python3
"""
    A seesion clss
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import Dict, TypeVar
from uuid import uuid4, UUID


class SessionAuth(Auth):
    """ Session Auth Class"""
    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID
            Args:
                user_id: user id
            Return:
                the session id
        """
        if user_id is None or type(user_id) is not str:
            return None

        session_id: str = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """retrieving a link between a User ID and a Session ID.
            Args:
                session_id: session id
            Return:
                the value (the User ID) for the key session_id
        """
        if session_id is None or type(session_id) is not str:
            return None

        user_id: str = self.user_id_by_session_id.get(session_id)

        return user_id

    def current_user(self, request=None):
        """Gets a User based on session id
            Args:
                request: to lookup
            Return:
                a user
        """
        session_id: str = self.session_cookie(request)
        user_id: str = self.user_id_for_session_id(session_id)
        user: TypeVar('User') = User.get(user_id)

        return user
