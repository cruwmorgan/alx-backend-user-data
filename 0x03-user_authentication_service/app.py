#!/usr/bin/env python3
"""
    A Flask APp
"""
from flask import Flask, jsonify, request, abort, redirect, make_response
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def hello() -> str:
    """ Greeting in French """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
