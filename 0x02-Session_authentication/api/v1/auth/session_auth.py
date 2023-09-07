#!/usr/bin/env python3
"""
    A seesion clss
"""
from api.v1.auth.auth import Auth
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
