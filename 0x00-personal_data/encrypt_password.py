#!/usr/bin/env python3
"""
    Encrypting passwords
"""
import bcrypt


def hash_password(password: str = '') -> bytes:
    """
        Hashed the password

        Args:
            password: string to hashed

        Return:
            hashed password
    """
    hashed = bcrypt.hashpw(password.encode('utf-8'),
                           bcrypt.gensalt(prefix=b"2b"))

    return hashed
