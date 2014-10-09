from flask import request
from flask.ext.restful import  Resource

from tracker.extensions import db, api
from tracker.models import User
from tracker.forms import UserCreateForm, SessionCreateForm
from flask.ext.login import login_user

class UserView(Resource):
    
    def post(self):
        form = UserCreateForm()
        
        if not form.validate_on_submit():
            return form.errors, 422
        
        user = User()
        
        form.populate_obj(user)
        
        db.session.add(user)
        db.session.commit()
        
        return 201

class SessionView(Resource):

    def post(self):
        form = SessionCreateForm()
        
        if not form.validate_on_submit():
            return form.errors, 422

        user, authenticated = User.authenticate(form.email.data,
                                    form.password.data)

        if user and authenticated:
            if login_user(user):
                return 200
        
        return "Login Failed", 401

api.add_resource(UserView, '/api/v1/user')
api.add_resource(SessionView, '/api/v1/session', endpoint = 'login')

