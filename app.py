from flask import request, abort, jsonify, Flask
from flask_cors import CORS
from sqlalchemy import exc
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # Routes
    @app.route("/")
    def index():
        return "Welcome to the casting agency!"

    @app.route("/login")
    def login():
        return jsonify({
            "login": "login successful"
        })

    @app.route("/actors", methods=['GET'])
    @requires_auth(permission='get:actors')
    def get_actors(*args, **kwargs):
        """Retrieves all actors"""
        actors = Actor.query.order_by(Actor.id)
        actor_list = [actor.formatted() for actor in actors]

        return jsonify({
            "success": True,
            "status_code": 200,
            "actors": actor_list,
            "total_actors": len(actor_list)
        })

    @app.route("/movies", methods=['GET'])
    @requires_auth(permission='get:movies')
    def get_movies(jwt):
        """Retrieves all movies"""
        movies = Movie.query.order_by(Movie.id)
        movie_list = [movie.formatted() for movie in movies]

        return jsonify({
            "success": True,
            "status_code": 200,
            "movies": movie_list,
            "total_movies": len(movie_list)
        })

    @app.route("/actors/<int:actor_id>", methods=['GET'])
    @requires_auth(permission='get:actors')
    def get_actor(jwt, actor_id):
        """Gets an individual actor."""
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
        """Gets an individual movie."""
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
        """Deletes an actor."""
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
        """Deletes a movie."""
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
        """Creates a movie."""
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
        """Creates an actor."""
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
        """Edits a movies data."""
        movie = Movie.query.get(movie_id)

        if not movie:
            abort(404)

        try:
            body = request.get_json()
            title = body.get('title', None)
            release_date = body.get('release_date', None)

            if title:
                movie.title = title
            if release_date:
                movie.release_date = release_date

            movie.update()

            return jsonify({
                "success": True,
                "status_code": 200,
                "movie": movie.formatted()
            })
        except exc.SQLAlchemyError:
            abort(422)

    @app.route("/actors/<int:actor_id>", methods=['PATCH'])
    @requires_auth(permission='edit:actor')
    def edit_actor(payload, actor_id):
        """Edits an actors data."""
        actor = Actor.query.get(actor_id)

        if not actor:
            abort(404)

        try:
            body = request.get_json()
            name = body.get('name', None)
            age = body.get('age', None)
            gender = body.get('gender', None)

            if name:
                actor.name = name
            if age:
                actor.age = age
            if gender:
                actor.gender = gender

            actor.update()

            return jsonify({
                "success": True,
                "status_code": 200,
                "actor": actor.formatted()
            })
        except exc.SQLAlchemyError:
            abort(422)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
