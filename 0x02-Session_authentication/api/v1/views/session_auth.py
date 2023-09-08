#!/usr/bin/env python3
"""
    Module that handles all routes for the Session authentication.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from os import getenv
from models.user import User
from typing import TypeVar, List


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def newlogin():
    """Module for login
        Return:
            A user session and credential
    """
    email = request.form.get('email')
    if not email:
        return make_response(jsonify({"error": "email missing"}), 400)

    password = request.form.get('password')
    if not password:
        return make_response(jsonify({"error": "password missing"}), 400)

    user_exist = User.search({"email": email})

    if len(user_exist) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    from api.v1.app import auth
    for user in user_exist:
        if (user.is_valid_password(password)):
            session_id = auth.create_session(user.id)
            SESSION_NAME = getenv('SESSION_NAME')
            response = make_response(user.to_json())
            response.set_cookie(SESSION_NAME, session_id)
            return response

    return make_response(jsonify({"error": "wrong password"}), 401)
