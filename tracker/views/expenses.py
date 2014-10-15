from flask import request
from flask.ext.restful import  Resource

from tracker.extensions import db, api
from tracker.models import Expense
from tracker.forms import ExpenseCreateForm, ExpenseSearchForm
from flask.ext.login import current_user
from tracker.decorators import login_required
from tracker.utils import seconds_since_week

class ExpenseView(Resource):

	@login_required
	def post(self):
		form = ExpenseCreateForm()

		if not form.validate_on_submit():
			return form.errors, 422

		expense = Expense()
		form.populate_obj(expense)
		expense.user = current_user
		expense.save()

		return 201

class ExpenseEditView(Resource):

	@login_required
	def put(self,expense_id):
		form = ExpenseCreateForm()
		if not form.validate_on_submit():
			return form.errors, 422
		expense = Expense.query.get_or_404(expense_id)
		form.populate_obj(expense)
		expense.save()


class ExpenseListView(Resource):
	
	@login_required
	def get(self):
		expenses = Expense.get_user_expenses()
		data = [expense.to_dict() for expense in expenses]
		total_amount = sum([x.amount for x in expenses])
		return {'total_amount':total_amount,'expenses':data}

class ExpenseAnalytics(Resource):

	@login_required
	def get(self,week):
		start,end = seconds_since_week(week)
		expenses = Expense.get_week_expenses(start,end)
		data = [expense.to_dict() for expense in expenses]
		total_amount = sum([x.amount for x in expenses])
		return {'total_amount':total_amount,'expenses':data}

class ExpenseSearch(Resource):

	@login_required
	def post(self):
		form = ExpenseSearchForm()

		if not form.validate_on_submit():
			return form.errors, 422

		expenses =  form.get_filters().all()
		data = [expense.to_dict() for expense in expenses]
		total_amount = sum([x.amount for x in expenses])
		return {'total_amount':total_amount,'expenses':data}


api.add_resource(ExpenseView, '/api/v1/expense', endpoint = 'expense')
api.add_resource(ExpenseEditView, '/api/v1/expense/<int:expense_id>', endpoint = 'expenseEdit')
api.add_resource(ExpenseListView, '/api/v1/expenses/', endpoint = 'expenses')
api.add_resource(ExpenseAnalytics, '/api/v1/expenses/week/<int:week>', endpoint = 'expenseAnalytics')
api.add_resource(ExpenseSearch, '/api/v1/expenses/search/', endpoint = 'expenseSearch')
