from operator import ne
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import setup_db,  Movies,Actors, db_drop_and_create_all
from flask_cors import CORS
from auth import AuthError, requires_auth


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  
  # db_drop_and_create_all()
  @app.after_request
  def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response
  @app.route('/')
  def get_greeting():
      # excited = os.environ['EXCITED']
      greeting = "Hello" 
      # if excited == 'true': greeting = greeting + "!!!!!"
      return greeting

  @app.route('/coolkids')
  def be_cool():
      return "Be cool, man, be coooool! You're almost a FSND grad!"

  # GET Movies *ITS WORKING*
  @app.route('/movies')
  def movies():
      movies = Movies.query.all()
      formatted_movies=[movie.format() for movie in movies]

      if len(movies)==0:
        abort(404)

      return jsonify({
          'success':True,
          "movies": formatted_movies
          }),200

  
  # POST Movies *ITS WORKING*
  @app.route('/movies',methods=['POST'])
  @requires_auth('post:movies')
  def post_movies(jwt):
      body=request.get_json()
      new_title= body.get('title')
      new_release_date=body.get('release_date')
      
      try:
          movie = Movies(title=new_title,release_date=new_release_date)
          movie.insert()
          formatted_movie = movie.format()
          return  jsonify({
              'success':True,
              'movies': formatted_movie
              }),200
      except:
        abort(422)

  # PATCH Movies

  @app.route('/movies/<int:id>',methods=['PATCH'])
  @requires_auth('patch:movies')
  def patch_movie(jwt,id):
      movie = Movies.query.filter(Movies.id==id).one_or_none()

      if movie is None:
          abort(404)
      body=request.get_json()
      movie.title= body.get('title')
      movie.new_release_date=body.get('release_date')
      movie.update()
      formatted_movie = movie.format()
      return  jsonify({
          'success':True,
          "movie": formatted_movie
          }),200

  # DELETE Movies *ITS WORKING*

  @app.route('/movies/<int:id>',methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(jwt,id):
      try:
        movie = Movies.query.filter(Movies.id==id).one_or_none()
        if movie is None:
            abort(404)

        movie.delete()
        return jsonify({
            "success": True,
            "delete": id
            }),200
      except:
          abort(400)

  # GET Actors *ITS WORKING*
  @app.route('/actors')
  def actors():
      actors = Actors.query.all()
      formatted_actors=[actor.format() for actor in actors]

      if len(actors)==0:
        abort(404)

      return jsonify({
          'success':True,
          "actors": formatted_actors
          }),200


  # Error Handling

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
      }), 422



  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error':404,
      'message': 'Not found'
    }),404


  @app.errorhandler(AuthError)
  def auth_error(e):
        return jsonify({
            "success": False,
            "error": e.status_code,
            "message": e.error
        }), e.status_code


  @app.errorhandler(401)
  def unauthorized(error):
    return jsonify({
        "success": False,
        "error":401,
        "message": 'Unauthorized'
      }),401

  @app.errorhandler(403)
  def forbidden(error):
        return jsonify({
            'success': False,
            'error':403,
            'message': 'Forbidden'
        }),403

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
        'success': False,
        'error':400,
        'message': 'Bad request'
      }),400

  return app
    
  
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='127.0.0.1',port=port,debug=True)

# https://dev-d2w4honx.us.auth0.com/authorize?audience=dev&response_type=token&client_id=0nHVQExqXT4QGjbVrfJ40RL2cg9Ms351&redirect_uri=https://127.0.0.1:8080/login-results

