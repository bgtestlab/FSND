import os, sys, json
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
    
  # ROUTES
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


  @app.route('/movies', methods=['POST'])
  @requires_auth(permission='post:actors')
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
  @ error handler for AuthError
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)