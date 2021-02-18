import os
import sys
import json
from flask import (
    Flask,
    request,
    abort,
    jsonify
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # Routes
    '''
      GET /actors
          it is for retrieving actors data
          it requires the 'get:actors' permission
      returns status code 200 and json {"success": True, "actors": actors} where actors is the list of actors
          or appropriate status code indicating reason for failure
    '''
    @app.route('/actors')
    @requires_auth(permission='get:actors')
    def get_actors(payload):
        data = Actor.query.all()
        actors = []

        if data:
            actors = [actor.format() for actor in data]

        return jsonify({
            'success': True,
            'actors': actors
        })

    '''
      GET /movies
          it is for retrieving movies data
          it requires the 'get:movies' permission
      returns status code 200 and json {"success": True, "actors": movies} where actors is the list of movies
          or appropriate status code indicating reason for failure
    '''
    @app.route('/movies')
    @requires_auth(permission='get:movies')
    def get_movies(payload):
        data = Movie.query.all()
        movies = []

        if data:
            movies = [movie.format() for movie in data]

        return jsonify({
            'success': True,
            'movies': movies
        })

    '''
      POST /actors
          it creates a new row in the actors table
          it requires the 'post:actors' permission
      returns status code 200 and json {"success": True, "actors": actor} where actor containing only the newly created actor
          or appropriate status code indicating reason for failure
    '''
    @app.route('/actors', methods=['POST'])
    @requires_auth(permission='post:actors')
    def post_actors(payload):
        body = request.get_json()
        req_name = body.get('name')
        req_age = body.get('age')
        req_gender = body.get('gender')

        try:
            actor = Actor(
                name=req_name,
                age=req_age,
                gender=req_gender
            )
            actor.insert()

            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        except SQLAlchemyError as e:
            print(e)

    '''
      POST /movies
          it creates a new row in the movies table
          it requires the 'post:movies' permission
      returns status code 200 and json {"success": True, "movies": movie} where movie containing only the newly created movie
          or appropriate status code indicating reason for failure
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth(permission='post:movies')
    def post_movies(payload):
        body = request.get_json()
        req_title = body.get('title')
        req_release_date = body.get('release_date')

        try:
            movie = Movie(
                title=req_title,
                release_date=req_release_date
            )
            movie.insert()

            return jsonify({
                'success': True,
                'movie': movie.format()
            })
        except SQLAlchemyError as e:
            print(e)

    '''
      PATCH /actors/<id>
          where <id> is the existing actor id
          it responds with a 404 error if <id> is not found
          it updates the corresponding row for <id>
          it requires the 'patch:actors' permission
      returns status code 200 and json {"success": True, "actors": actor} where actor containing only the updated actor
          or appropriate status code indicating reason for failure
    '''
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth(permission='patch:actors')
    def modify_actor(payload, actor_id):
        try:
            actor = Actor.query.filter(
                Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            body = request.get_json()
            req_age = body.get('age')
            req_gender = body.get('gender')

            actor.age = req_age
            actor.gender = req_gender
            actor.update()

            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        except SQLAlchemyError as e:
            print(e)

    '''
      PATCH /movies/<id>
          where <id> is the existing movie id
          it responds with a 404 error if <id> is not found
          it updates the corresponding row for <id>
          it requires the 'patch:movies' permission
      returns status code 200 and json {"success": True, "movies": movie} where actor containing only the updated movie
          or appropriate status code indicating reason for failure
    '''
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth(permission='patch:movies')
    def modify_movie(payload, movie_id):
        try:
            movie = Movie.query.filter(
                Movie.id == movie_id).one_or_none()

            if movie is None:
                abort(404)

            body = request.get_json()
            req_release_date = body.get('release_date')

            movie.release_date = req_release_date
            movie.update()

            return jsonify({
                'success': True,
                'movie': movie.format()
            })
        except SQLAlchemyError as e:
            print(e)

    '''
      DELETE /actors/<id>
          where <id> is the existing model id
          it responds with a 404 error if <id> is not found
          it deletes the corresponding row for <id>
          it requires the 'delete:actors' permission
      returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
          or appropriate status code indicating reason for failure
    '''
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth(permission='delete:actors')
    def delete_actor(payload, actor_id):
        try:
            actor = Actor.query.filter(
                Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            actor.delete()

            return jsonify({
                'success': True,
                'delete': actor_id
            })
        except SQLAlchemyError as e:
            print(e)

    '''
      DELETE /actors/<id>
          where <id> is the existing model id
          it responds with a 404 error if <id> is not found
          it deletes the corresponding row for <id>
          it requires the 'delete:movies' permission
      returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
          or appropriate status code indicating reason for failure
    '''
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth(permission='delete:movies')
    def delete_movie(payload, movie_id):
        try:
            movie = Movie.query.filter(
                Movie.id == movie_id).one_or_none()

            if movie is None:
                abort(404)

            movie.delete()

            return jsonify({
                'success': True,
                'delete': movie_id
            })
        except SQLAlchemyError as e:
            print(e)

    # Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    '''
    error handler for AuthError
        error handler should conform to general task above
    '''
    @app.errorhandler(AuthError)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'unauthorized'
        }), 401

    return app


app = create_app()

# Default port
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
