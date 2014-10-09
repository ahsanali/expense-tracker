from flask import request
from flask.ext.restful import  Resource

from tracker.extensions import db, api
from tracker.models import Comment, Expense
from tracker.forms import CommentCreateForm
from flask.ext.login import login_required, current_user
from tracker.utils import seconds_since_week

class CommentView(Resource):

	@login_required
	def post(self,expense_id):
		form = CommentCreateForm()

		if not form.validate_on_submit():
			return form.errors, 422

		comment = Comment()
		form.populate_obj(comment)
		comment.expense_id = expense_id
		comment.user = current_user
		comment.save()

		return comment.to_dict()

class CommentListView(Resource):
	
	@login_required
	def get(self,expense_id):
		comments = Expense.get_comments(expense_id)
		return [comment.to_dict() for comment in comments]


api.add_resource(CommentView, '/api/v1/comment/<int:expense_id>', endpoint = 'comment')
api.add_resource(CommentListView, '/api/v1/comments/<int:expense_id>', endpoint = 'comments')

