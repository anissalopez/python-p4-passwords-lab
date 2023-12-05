#!/usr/bin/env python3

from flask import make_response, request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username'],
            password_hash=json['password']
        )
        
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return user.to_dict(), 201

class CheckSession(Resource):
    def get(self):
        
        user_id = session.get('user_id')
        if user_id:
            user = User.query.filter(User.id == user_id).first()

            
         
            return user.to_dict(), 200
        
        return make_response("", 204)

class Login(Resource):
    def post(self):
        json_data = request.get_json()
        if 'username' in json_data and 'password' in json_data:
            username = json_data['username']
            # user = User.query.filter_by(username=username)
            user = User.query.filter(User.username == username).first()
            password = json_data['password']

        # username = request.get_json()['username']
        # user = User.query.filter_by(username=username).first()

        # password = request.get_json()['password']
        # print(request.get_json())

            if user.authenticate(password):
                session['user_id'] = user.id
                return user.to_dict(), 200

        return {'error': 'Invalid username or password'}, 401

    

class Logout(Resource):
    def delete(self):

        session['user_id'] = None
        
        return {}, 204
    

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
