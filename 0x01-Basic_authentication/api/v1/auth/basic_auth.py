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

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
            method for extracting email and password from auth header

            Args:
                decoded_base64_authorization_header: a string decoded

            Return:
                the user email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None or\
           type(decoded_base64_authorization_header) != str or\
           ':' not in decoded_base64_authorization_header:

            return (None, None)

        credentials = decoded_base64_authorization_header.split(':', 1)

        return (credentials[0], credentials[1])

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """
         method for extracting user instance fom email and password
            Args:
                user_email: a user email
                user_pwd: user password
            Return:
                the User instance based on his email and password
        """
        if user_email is None or type(user_email) != str or\
           user_pwd is None or type(user_pwd) != str:\

            return None

        try:
            exist_user: List[TypeVar('User')]
            exist_user = User.search({"email": user_email})
        except Exception:
            return None

        for user in exist_user:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
            method that extracts the user instance from base64 auth header

            Args:
              request:auth header

            Return:
            : the User instance for a request
        """
        header: str = self.authorization_header(request)

        if header is None:
            return None

        auth_head64: str = self.extract_base64_authorization_header(header)

        if auth_head64 is None:
            return None

        decode_auth: str = self.decode_base64_authorization_header(auth_head64)

        if decode_auth is None:
            return decode_auth

        mail: str
        passwd: str
        mail, passwd = self.extract_user_credentials(decode_auth)

        if mail is None or passwd is None:
            return None

        user_curr = self.user_object_from_credentials(mail, passwd)

        return user_curr
