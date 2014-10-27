# -*- coding: utf-8 -*-

from tracker.models import User, Expense, Comment

from tracker.tests import TestCase
from tracker.utils import MALE, FEMALE
from werkzeug import generate_password_hash
from flask.ext.login import login_user, current_user
import datetime

class TestUser(TestCase):

    def test_get_current_user(self):
    	""" Test default user """
        assert User.query.count() == 1

    def test_check_password(self):
    	""" Test if password is checked accuratley """
    	details = dict(
	    		name = 'tester',
	    		email = 'test@test.com',
	    		password = 'abcdef',
	    		)
    	user = User(**details)
    	assert user.check_password(details['password'])
    	assert not user.check_password(details['password']+"12")

    def test_authentication(self):
    	""" Test authentication of user """
    	user,authenticated = User.authenticate(self.demo_user_details["email"],self.demo_user_details["password"])
    	assert user.id == self.demo_user.id 
    	assert authenticated

    def test_user_creation(self):
    	""" Test if user details are stored acurately in the database """
    	details = dict(
	    		name = 'tester',
	    		email = 'test@test.com',
	    		password = 'abcdef',
	    		age = 23,
	    		phone = "+12377123123",
	    		sex_code = MALE
	    		)
    	user = User(**details)
    	user.save()
    	user_id = user.id
    	del(user)
    	created_user = User.query.get(user_id)
    	assert created_user
    	assert created_user.name == details['name']
    	assert created_user.email == details['email']
    	assert created_user.password 
    	assert created_user.age == details['age']
    	assert created_user.phone == details['phone']
    	assert created_user.sex_code == details['sex_code'] 

class TestExpense(TestCase):


	def test_user_expenses(self):
		""" Test expense filteration by logged in user """

		expenses = Expense.get_user_expenses()
		assert len(expenses) == 1
		assert expenses[0] == self.expense

	def test_week_expenses(self):
		""" Test expense filteration by logged in user and expense_time """
		expenses = Expense.get_week_expenses(self.expense_details['expense_time']-100,self.expense_details['expense_time']+100)
		assert len(expenses) == 1
		assert expenses[0] == self.expense		


	def test_expense_creation(self):
		""" Test if the expense is created fine in the database """
		details = dict(
            description = "Guitar",
            expense_time = int(datetime.datetime.now().strftime("%s")) * 1000,
            amount = 120.00,
            user = self.demo_user
            )

		expense = Expense(**details)
		expense.save()
		expense_id = expense.id
		del(expense)
		created_expense = Expense.query.get(expense_id)
		assert created_expense
		assert created_expense.description == details["description"]
		assert created_expense.expense_time == details["expense_time"]
		assert created_expense.amount == details["amount"]
		assert created_expense.user.id == self.demo_user.id

class TestComments(TestCase):

	def test_expense_comments(self):
		""" Test expense comments """
		comments = Expense.get_comments(self.expense.id)
		assert len(comments) == 1
		assert comments[0] == self.comment

	def test_comment_creation(self):
		""" Test if the comments are created fine in the database """
		details = dict(
            text = "should buy from super market",
            user = self.demo_user,
            expense = self.expense
            )

		comment = Comment(**details)
		comment.save()
		comment_id = comment.id
		del(comment)
		created_comment = Comment.query.get(comment_id)
		assert created_comment
		assert created_comment.text == details["text"]
		assert created_comment.user.id == self.demo_user.id
		assert created_comment.expense.id == self.expense.id
