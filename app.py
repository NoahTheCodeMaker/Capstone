import os, traceback
from flask import Flask, jsonify, redirect, abort, request
from auth import requires_auth, AuthError
from models import setup_db, Actors, Movies, db
from flask_cors import CORS

LOGIN_LINK = os.environ['LOGIN_LINK']

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # Route that works for anyone with the link
    @app.route('/', methods=['GET'])
    def capstone_intro():
        try:
            return jsonify({
            "success": True,
            "message": "Welcome to my Capstone Project! Please navigate to /login to log into an account!"
        })
        except:
            traceback.print_exc()
            abort(500)
    
    # Login route that works for anyone with the link
    @app.route('/login', methods=['GET'])
    def login():
        return(redirect(location=LOGIN_LINK))

    # You can check the /auth endpoint to see
    # if the login worked with your own jwt,
    # but the rest of the endpoints need my 
    # custom roles on the tokens provided
    @app.route('/auth', methods=['GET'])
    @requires_auth("")
    def authorize(payload):
        return jsonify({
            "success": True,
            "payload": payload
        })
    
    # Endpoint for viewing actors.
    @app.route('/actors', methods=['GET'])
    @requires_auth('read:actors')
    def actor_view(payload):
        try:
            formatted_actors = []
            actors = Actors.query.all()
            for actor in actors:
                formatted_actors.append({
                    "id": actor.id,
                    "name": actor.name,
                    "age": actor.age,
                    "gender": actor.gender,
                })
            return jsonify({
                "success": True,
                "actors": formatted_actors
            })
        except:
            traceback.print_exc()
            abort(500)

    # Endpoint for viewing single actor by id.
    @app.route('/actors/<int:id>', methods=['GET'])
    @requires_auth('read:actors')
    def single_actor_view(payload, id):
        try:
            actor = Actors.query.filter_by(id=id).one()
            return jsonify({
                "success": True,
                "actor": actor.format()
            })
        except:
            traceback.print_exc()
            abort(500)

    # Endpoint for viewing movies.
    @app.route('/movies', methods=['GET'])
    @requires_auth('read:movies')
    def movie_view(payload):
        try:
            formatted_movies = []
            movies = Movies.query.all()
            for movie in movies:
                formatted_movies.append({
                    "id": movie.id,
                    "title": movie.title,
                    "release_date": movie.release_date
                })
            return jsonify({
                "success": True,
                "movies": formatted_movies
            })
        except:
            traceback.print_exc()
            abort(500)

    # Endpoint for viewing single movie by id.
    @app.route('/movies/<int:id>', methods=['GET'])
    @requires_auth('read:movies')
    def single_movie_view(payload, id):
        try:
            movie = Movies.query.filter_by(id=id).one()
            return jsonify({
                "success": True,
                "movie": movie.format()
            })
        except:
            traceback.print_exc()
            abort(500)

    # Endpoint for creating actors
    @app.route('/actors', methods=['POST'])
    @requires_auth('create:actors')
    def create_actor(payload):
        try:
            name = request.get_json().get("name", None)
            age = request.get_json().get("age", None)
            gender = request.get_json().get("gender", None)
            new_actor = Actors(
                name=name,
                age=age,
                gender=gender
            )
            db.session.add(new_actor)
            db.session.commit()
            return jsonify({
                "success": True,
                "actor": new_actor.format()
            })
        except:
            db.session.rollback()
            traceback.print_exc()
            abort(422)

    # Endpoint for creating movies
    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movies')
    def create_movie(payload):
        try:
            title = request.get_json().get("title", None)
            release_date = request.get_json().get("release_date", None)
            new_movie = Movies(
                title=title,
                release_date=release_date
            )
            db.session.add(new_movie)
            db.session.commit()
            return jsonify({
                "success": True,
                "movie": new_movie.format()
            })
        except:
            db.session.rollback()
            traceback.print_exc()
            abort(422)

    # Endpoint for editing actors
    @app.route('/actors', methods=['PATCH'])
    @requires_auth('edit:actors')
    def edit_actor(payload):
        try:
            actor_id = request.get_json().get("id", None)
            name = request.get_json().get("name", None)
            age = request.get_json().get("age", None)
            gender = request.get_json().get("gender", None)
            edited_actor = Actors.query.get(actor_id)
            edited_actor.name = name
            edited_actor.age = age
            edited_actor.gender = gender
            db.session.commit()
            return jsonify({
                "success": True,
                "actor": edited_actor.format()
            })
        except:
            db.session.rollback()
            traceback.print_exc()
            abort(422)

    # Endpoint for editing movies
    @app.route('/movies', methods=['PATCH'])
    @requires_auth('edit:movies')
    def edit_movie(payload):
        try:
            movie_id = request.get_json().get("id", None)
            title = request.get_json().get("title", None)
            release_date = request.get_json().get("release_date", None)
            edited_movie = Movies.query.get(movie_id)
            edited_movie.title = title
            edited_movie.release_date = release_date
            db.session.commit()
            return jsonify({
                "success": True,
                "movie": edited_movie.format()
            })
        except:
            db.session.rollback()
            traceback.print_exc()
            abort(422)

    # Endpoint for deleting actors
    @app.route('/actors/delete', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload):
        try:
            actor_id = request.get_json().get("id", None)
            Actors.query.filter_by(id=actor_id).delete()
            db.session.commit()
            return jsonify({
                "success": True,
                "deleted_actor_id": actor_id
            })
        except:
            traceback.print_exc()
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    # Alternate endpoint for deleting actors
    @app.route('/actors', methods=['DELETE'])
    @requires_auth('delete:actors')
    def axios_delete_actor(payload):
        try:
            actor_id = request.args.get('id')
            Actors.query.filter_by(id=actor_id).delete()
            db.session.commit()
            return jsonify({
                "success": True,
                "deleted_actor_id": actor_id
            })
        except:
            traceback.print_exc()
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()

    # Endpoint for deleting movies
    @app.route('/movies/delete', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload):
        try:
            movie_id = request.get_json().get("id", None)
            Movies.query.filter_by(id=movie_id).delete()
            db.session.commit()
            return jsonify({
                "success": True,
                "deleted_movie_id": movie_id
            })
        except:
            traceback.print_exc()
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    # Alternate endpoint for deleting movies
    @app.route('/movies', methods=['DELETE'])
    @requires_auth('delete:movies')
    def axios_delete_movie(payload):
        try:
            movie_id = request.args.get('id')
            Movies.query.filter_by(id=movie_id).delete()
            db.session.commit()
            return jsonify({
                "success": True,
                "deleted_movie_id": movie_id
            })
        except:
            traceback.print_exc()
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()

    # Forcing errors for error tests

    @app.route('/400errortest', methods=['GET'])
    def test400():
        if request.method == 'GET':
            abort(400)

    @app.route('/422errortest', methods=['GET'])
    def test422():
        if request.method == 'GET':
            abort(422)

    @app.route('/500errortest', methods=['GET'])
    def test500():
        if request.method == 'GET':
            abort(500)

    # Error handlers

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
        }), 400 

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
        }), 404
    
    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable entity"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
        }), 500
    
    # Authorization error handler
    @app.errorhandler(AuthError)
    def auth_error(payload):
        return jsonify({
            "success": False,
            "error": payload.status_code,
            "message": payload.error
        }), payload.status_code
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run()
