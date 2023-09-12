#!/usr/bin/env python3
"""
    Auth module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Bcrypt a password
        Args:
            password: a string

        Return;
            bytes
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
