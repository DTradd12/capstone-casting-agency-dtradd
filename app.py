from flask import request, abort, jsonify, Flask
from flask_cors import CORS
from sqlalchemy import exc
from database.models import setup_db, db_drop_and_create_all, Movie, Actor
from auth.auth import AuthError, requires_auth

database_path = "postgres://postgres:password:5432/castingagency"


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # db_drop_and_create_all()

    # Routes
    @app.route("/")
    def index():
        movies = Movie.query.order_by(Movie.id)
        actors = Actor.query.order_by(Actor.id)
        movie_list = [movie.formatted() for movie in movies]
        actor_list = [actor.formatted() for actor in actors]

        return jsonify({
            "success": True,
            "status_code": 200,
            "movies": movie_list,
            "actors": actor_list
        })

    @app.route("/login")
    def login():
        return jsonify({
            "login": "login successful"
        })

    @app.route("/actors", methods=['GET'])
    @requires_auth(permission='get:actors')
    def get_actors(*args, **kwargs):
        actors = Actor.query.order_by(Actor.id)
        actor_list = [actor.formatted() for actor in actors]

        if len(actor_list) == 0:
            abort(404)
        else:
            return jsonify({
                "success": True,
                "status_code": 200,
                "actors": actor_list
            })

    @app.route("/movies", methods=['GET'])
    @requires_auth(permission='get:movies')
    def get_movies(jwt):
        movies = Movie.query.order_by(Movie.id)
        movie_list = [movie.formatted() for movie in movies]

        if len(movie_list) == 0:
            abort(404)
        else:
            return jsonify({
                "success": True,
                "status_code": 200,
                "movies": movie_list
            })

    @app.route("/actors/<int:actor_id>", methods=['GET'])
    @requires_auth(permission='get:actors')
    def get_actor(jwt, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)
        else:
            return jsonify({
                "success": True,
                "status_code": 200,
                "actor": actor.formatted()
            })

    @app.route("/movies/<int:movie_id>", methods=['GET'])
    @requires_auth(permission='get:movies')
    def get_movie(jwt, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)
        else:
            return jsonify({
                "success": True,
                "status_code": 200,
                "movie": movie.formatted()
            })

    @app.route("/actors/<int:actor_id>", methods=['DELETE'])
    @requires_auth(permission='delete:actor')
    def delete_actor(jwt, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(422)
        else:
            actor.delete()
            return jsonify({
                "success": True,
                "status_code": 200,
                "deleted": actor.id
            })

    @app.route("/movies/<int:movie_id>", methods=['DELETE'])
    @requires_auth(permission='delete:movie')
    def delete_movie(jwt, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(422)
        else:
            movie.delete()
            return jsonify({
                "success": True,
                "status_code": 200,
                "deleted": movie.id
            })

    @app.route("/movies/create", methods=['POST'])
    @requires_auth(permission='post:movie')
    def add_movie(jwt):
        body = request.get_json()

        try:
            new_movie = Movie(body['title'], body['release_date'])
            new_movie.create()

            return jsonify({
                "success": True,
                "status_code": 200,
                "movie": new_movie.formatted()
            })
        except exc.SQLAlchemyError:
            abort(409)

    @app.route("/actors/create", methods=['POST'])
    @requires_auth(permission='post:actor')
    def add_actor(jwt):
        body = request.get_json()

        try:
            new_actor = Actor(body['name'], body['age'], body['gender'])
            new_actor.create()

            return jsonify({
                "success": True,
                "status_code": 200,
                "actor": new_actor.formatted()
            })
        except exc.SQLAlchemyError:
            abort(409)

    @app.route("/movies/<int:movie_id>", methods=['PATCH'])
    @requires_auth(permission='edit:movie')
    def edit_movie(payload, movie_id):
        body = request.get_json()

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if not movie:
            abort(404)
        else:
            movie.title = body['title']
            movie.release_date = body['release_date']

            movie.update()

            return jsonify({
                "success": True,
                "status_code": 200,
                "movie": movie.formatted()
            })

    @app.route("/actors/<int:actor_id>", methods=['PATCH'])
    @requires_auth(permission='edit:actor')
    def edit_actor(payload, actor_id):
        body = request.get_json()

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if not actor:
            abort(404)
        else:
            actor.name = body['name']
            actor.age = body['age']
            actor.gender = body['gender']

            actor.update()

            return jsonify({
                "success": True,
                "status_code": 200,
                "actor": actor.formatted()
            })

    # Error Handling
    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

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
            "message": "not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(409)
    def duplicate_entry(error):
        return jsonify({
            "success": False,
            "error": 409,
            "message": "duplicate of an existing entry"
        }), 409

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    return app


app = create_app()

# Default port:
if __name__ == '__main__':
    app.run()
