#!/usr/bin/env python3
"""
    Module of Basicauth
"""
from api.v1.auth.auth import Auth
from base64 import b64decode, binascii
from models.user import User
from typing import TypeVar, List


class BasicAuth(Auth):
    """
        Basic authentication class
    """
    def __init__(self):
        """Constructor"""

    def extract_base64_authorization_header(
                                            self, authorization_header: str
                                            ) -> str:
        """
            Method for extracting base64 authourization header

            Args:
                authorization_header: string containing base64
            Return: the Base64 part of the Authorization header
        """
        if authorization_header is None\
           or type(authorization_header) != str\
           or not authorization_header.startswith('Basic ')\
           and not authorization_header.endswith(' '):

            return None

        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
                                           self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
            method for extracting decoded base64 from auth header

            Arg:
                base64_authorization_header: Base64 header

            Return:
                 the decoded value of a Base64 string
        """
        if base64_authorization_header is None or\
           type(base64_authorization_header) != str:

            return None

        try:
            data_decode = b64decode(base64_authorization_header)
        except binascii.Error as err:
            return None

        return data_decode.decode('utf-8')
