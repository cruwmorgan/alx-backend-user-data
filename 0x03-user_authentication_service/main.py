#!/usr/bin/env python3
"""
    Main module for assertion of app functions
"""
import logging
import requests
from app import AUTH

logging.disable(logging.INFO)

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"

def register_user(email: str, password: str) -> None:
    """ Register new user
        Args:
            email: email address
            password: new password
        Return:
            assert ok
    """
    response = requests.post(f"{BASE_URL}/register", json={"email": email, "password": password})
    assert response.status_code == 200, "Registration failed with status code not equal to 201 (Created)"
    req = {"email": EMAIL, "message": "user created"}
    assert response.json() == req

def log_in_wrong_password(email: str, password: str) -> None:
    """ Login with error
        Args:
            email: email address
            password: new password
        Return:
            assert ok
    """
    response = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
    assert response.status_code == 401, "Login with wrong password should return 401 Unauthorized"

def log_in(email: str, password: str) -> str:
    """ Login sucess
        Args:
            email: email address
            password: new password
        Return:
            assert the values
    """
    response = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
    assert response.status_code == 200, "Login failed with status code not equal to 200 (OK)"
    req = {
        "email": email,
        "message": "logged in"
    }
    assert response.json() == req

def profile_unlogged() -> None:
    """ Login success
        Return:
            assert values
    """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403, "Profile request for unlogged user should return 403 Unauthorized"

def profile_logged(session_id: str) -> None:
    """ profile login with session id
        Args:
            session_id: session ID
        Return:
            assert values
    """
    headers = {"Authorization": f"Bearer {session_id}"}
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    assert response.status_code == 200, "Profile request for logged user failed with status code not equal to 200 (OK)"
    req = {
        "email": EMAIL,
    }
    assert response.json() == req

def log_out(session_id: str) -> None:
    """ Logout profile

        args:
            session_id: Session identificator

        return
            assert of the values
    """
    cookie = {
        "session_id": session_id
    }
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookie)
    assert response.status_code == 200, "Logou with status code not equal to 200 (OK)"

def reset_password_token(email: str) -> str:
    """ Reset password
        Args:
            email: email addresss of user
        Return:
            assert values
    """
    response = requests.post(f"{BASE_URL}/reset_password", json={"email": email})
    token = response.json().get('reset_token', None)
    req = {"email": email, "reset_token": token}
    assert response.status_code == 200, "Password reset request failed with status code not equal to 200 (OK)"
    assert response.json() == req
    return token

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Updates password of user
        Args:
            email: Email to identify user
            reset_token: Identifier to reset the password
            new_password: To change

        return
            assert of the values
    """
    response = requests.put(f"{BASE_URL}/update_password",
                            json={
                            "email": email,
                            "reset_token": reset_token,
                            "new_password": new_password}
                            )
    req = {"email": email, "message": "Password updated"}
    assert response.status_code == 200
    assert response.json() == req


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
