import os
from flask import Flask, jsonify, redirect, request
from auth import requires_auth
from models import setup_db
from flask_cors import CORS

LOGIN_LINK = os.environ['LOGIN_LINK']

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # Route that works for anyone with the link
    @app.route('/')
    def capstone_intro():
        return jsonify({
            "message": "Welcome to my Capstone Project!"
        })
    
    # Login route that works for anyone with the link
    @app.route('/login')
    def login():
        return(redirect(location=LOGIN_LINK))

    # You can check the /auth endpoint to see
    # if the login worked with your own jwt,
    # but the rest of the endpoints need my 
    # custom roles on the tokens provided
    @app.route('/auth')
    @requires_auth("")
    def authorize(payload):
        return jsonify({
            "success": True,
            "payload": payload
        })

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
