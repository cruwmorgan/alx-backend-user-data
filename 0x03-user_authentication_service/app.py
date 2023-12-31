#!/usr/bin/env python3
"""
    A Flask APp
"""
import logging
from flask import Flask, jsonify, request, abort, redirect, make_response
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth

logging.disable(logging.INFO)


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def hello() -> str:
    """ Greeting in French """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def new_register() -> str:
    """ Create a new user """
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        msg = {"message": "email already registered"}
        return jsonify(msg), 400

    msg = {"email": user.email, "message": "user created"}

    return jsonify(msg)


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def new_login() -> str:
    """ a login function"""
    # Get user credentials from form data
    email, password = request.form.get("email"), request.form.get("password")
    # Check if the user's credentials are valid
    if not AUTH.valid_login(email, password):
        abort(401)
    # Create a new session for the user
    session_id: str = AUTH.create_session(email)
    # Construct a response with a JSON payload
    response = jsonify({"email": email, "message": "logged in"})
    # Set a cookie with the session ID on the response
    response.set_cookie("session_id", session_id)
    # Return the response
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ a logout function """
    # Get the session ID from the "session_id" cookie in the request
    session_id = request.cookies.get("session_id")
    # Retrieve the user associated with the session ID
    user = AUTH.get_user_from_session_id(session_id)
    # If no user is found, abort the request with a 403 Forbidden error
    if user is None:
        abort(403)
    # Destroy the session associated with the user
    AUTH.destroy_session(user.id)
    # Redirect to the home route
    return redirect("/")


@app.route('/profile', methods=['GET'], strict_slashes=False)
def my_profile() -> str:
    """ a profile function """
    # get session id from cookie
    session_id = request.cookies.get("session_id")
    # Retrieve the user associated with the session ID
    user = AUTH.get_user_from_session_id(session_id)
    # If no user is found, abort the request with a 403 Forbidden error
    if user is None:
        abort(403)
    # Return the user's email as a JSON payload
    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """ a get_reset_password_token function """
    # Retrieve the email from the form data
    email = request.form.get("email")
    try:
        # Attempt to generate a reset token for the given email
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        # If the email is not found in the database, raise a 403 error
        abort(403)
    # Return a JSON payload containing the email and reset token
    return jsonify({"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """ Updates user password """
    # Retrieve the email, reset_token and new_password from the form data
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        # Attempt to update the password with the new password
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        # If the reset token is invalid, return an HTTP 403 error
        abort(403)
    # If the password was successfully updated, return a JSON object with the
    # user's email and a success message.
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
