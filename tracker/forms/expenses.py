from flask.ext.wtf import Form
 
from wtforms_alchemy import model_form_factory
from wtforms import StringField, DateField, IntegerField
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
    
class ExpenseSearchForm(Form):
	min_date = StringField('min_date')
	max_date = StringField('max_date')
	min_amount = IntegerField('min_amount')
	max_amount = IntegerField('max_amount')

	def get_filters(self):

		expenses = Expense.query
		
		if self.min_amount.data:
			expenses = expenses.filter(Expense.amount >  self.min_amount.data)
		if self.max_amount.data:
			expenses = expenses.filter(Expense.amount <  self.max_amount.data)
		if self.min_date.data:
			expenses = expenses.filter(Expense.expense_time >  self.min_date.data)
		if self.max_date.data:
			expenses = expenses.filter(Expense.expense_time <  self.max_date.data)
		
		expenses = expenses.order_by(Expense.created_time)
		
		return expenses
