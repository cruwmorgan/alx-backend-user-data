#!/usr/bin/env python3
"""
    Module of Basicauth
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
        Basic authentication class
    """
    def __init__(self):
        """Constructor"""
