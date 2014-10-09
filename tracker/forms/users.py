from flask.ext.wtf import Form
 
from wtforms_alchemy import model_form_factory
from wtforms import StringField
from wtforms.validators import DataRequired
 
from tracker.extensions import db
from tracker.models import User
 
BaseModelForm = model_form_factory(Form)
 
class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session
 
class UserCreateForm(ModelForm):
    password = StringField('password', validators=[DataRequired()])
    class Meta:
        model = User
    
class SessionCreateForm(Form):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])