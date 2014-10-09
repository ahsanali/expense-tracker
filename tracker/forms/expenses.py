from flask.ext.wtf import Form
 
from wtforms_alchemy import model_form_factory
from wtforms import StringField
from wtforms.validators import DataRequired
 
from tracker.extensions import db
from tracker.models import Expense
 
BaseModelForm = model_form_factory(Form)
 
class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session
 
class ExpenseCreateForm(ModelForm):

    class Meta:
        model = Expense
    
