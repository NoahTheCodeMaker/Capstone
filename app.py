import os
from flask import Flask, jsonify
from models import setup_db
from flask_cors import CORS

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def capstone_intro():
        return jsonify({
            "message": "Welcome to my Capstone Project!"
        })

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
