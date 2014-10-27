from tracker.tests import TestCase
import json
import datetime

class TestUserView(TestCase):

	def test_post(self):
		""" Test account creation"""
		data = dict(name = 'tester',
		email = 'test@test.com',
		password = 'abcdef',
		age = 23)
		response = self.client.post('/api/v1/user', data=data, follow_redirects=True)
		self.assert_201(response)

	def test_required_arguments(self):
		""" Test account creation arguments """
		data = dict(name = 'tester',
		email = 'test@test.com',
		password = 'abcdef',
		age = 23)
		required = ['name','password','email']
		for arg in required:
			data_copy = data.copy()
			del(data_copy[arg])
			response = self.client.post('/api/v1/user', data=data_copy, follow_redirects=True)
			self.assert_422(response)


class TestSessionView(TestCase):

	def test_post(self):
		"""Test Login"""
		self._logout()
		data = {
			'email': self.demo_user_details['email'],
			'password' : self.demo_user_details['password']
		}

		response = self.client.post('/api/v1/session',data = data ,follow_redirects=True)

		self.assert_200(response)

		data = {
			'email': self.demo_user_details['email'],
			'password' : "wrong password"
		}

		response = self.client.post('/api/v1/session',data = data ,follow_redirects=True)
		self.assert_401(response)


	def test_get(self):
		"""Testing Session"""

		self.login(self.demo_user_details['email'],self.demo_user_details['password'])
		response = self.client.get('/api/v1/session',follow_redirects=True)
		self.assert_200(response)
		user = json.loads(response.data)
		assert user['id'] == self.demo_user.id
		self._logout()
		response = self.client.get('/api/v1/session',follow_redirects=True)
		self.assert_401(response)


class TestExpenseView(TestCase):

	def test_post(self):
		"""Test Expense Creation"""
		self.login(self.demo_user_details['email'],self.demo_user_details['password'])
		data = dict(
            description = "Bananas",
            expense_time = 1414389745,
            amount = 12.00,
            )
		response = self.client.post('/api/v1/expense',data = data, follow_redirects=True)
		self.assert_201(response)

	def test_required_arguments(self):
		""" Test required arguments for expense creation """
		self.login(self.demo_user_details['email'],self.demo_user_details['password'])
		data = dict(
            description = "Bananas",
            expense_time = 1414389745,
            amount = 12.00,
            user = self.demo_user
            )

		required = ['description','expense_time','amount']

		for arg in required:
			data_copy = data.copy()
			del(data_copy[arg])
			response = self.client.post('/api/v1/expense', data=data_copy, follow_redirects=True)
			self.assert_422(response)

class TestExpenseListView(TestCase):

	def test_get(self):
		""" Test expenses list"""
		self.login(self.demo_user_details['email'],self.demo_user_details['password'])
		response = self.client.get('/api/v1/expenses/',follow_redirects=True)
		self.assert_200(response)
		expenses = json.loads(response.data)
		assert len(expenses['expenses']) == 1

		data = dict(
            description = "Bananas",
            expense_time = int(datetime.datetime.now().strftime("%s")) * 1000,
            amount = 12.00,
            )
		response = self.client.post('/api/v1/expense',data = data, follow_redirects=True)
		self.assert_201(response)


		response = self.client.get('/api/v1/expenses/',follow_redirects=True)
		self.assert_200(response)
		expenses = json.loads(response.data)
		assert len(expenses['expenses']) == 2
		total = 0
		for ex in expenses['expenses']:
			total = total + ex['amount']
		assert total == expenses['total_amount']


class TestExpenseEditView(TestCase):

	def test_put(self):
		""" Test edit expense """
		self.login(self.demo_user_details['email'],self.demo_user_details['password'])
		data = self.expense_details
		data['amount'] = 14.00
		response = self.client.put('/api/v1/expense/%s'%self.expense.id,data = data,follow_redirects=True)
		self.assert_200(response)

class TestExpenseAnalytics(TestCase):

	def test_get(self):
		""" Test expense filtering by date"""
		self.login(self.demo_user_details['email'],self.demo_user_details['password'])
		response = self.client.get("/api/v1/expenses/week/0",follow_redirects=True)
		self.assert_200(response)
		expenses = json.loads(response.data)
		assert len(expenses['expenses']) == 1

		expense_time = datetime.datetime.now() - datetime.timedelta(days = 7)
		expense_time = int(expense_time.strftime("%s"))

		data = dict(
            description = "Bananas",
            expense_time = expense_time*1000,
            amount = 17.00,
            )
		response = self.client.post('/api/v1/expense',data = data, follow_redirects=True)
		self.assert_201(response)

		response = self.client.get("/api/v1/expenses/week/1",follow_redirects=True)
		self.assert_200(response)
		expenses = json.loads(response.data)
		assert len(expenses['expenses']) == 1


class TestExpenseSearch(TestCase):

	def test_post(self):
		""" Test Expense Search """
		self.login(self.demo_user_details['email'],self.demo_user_details['password'])
		expense_time = datetime.datetime.now() - datetime.timedelta(days = 5)
		data = dict(
            description = "Bananas",
            expense_time = int(expense_time.strftime("%s")) * 1000,
            amount = 217.00,
            )
		response = self.client.post('/api/v1/expense',data = data, follow_redirects=True)
		self.assert_201(response)

		data = {"min_amount": 14}
		response = self.client.post('/api/v1/expenses/search/',data = data, follow_redirects=True)
		self.assert_200(response)
		expenses = json.loads(response.data)
		assert len(expenses['expenses']) == 1

		data = {"max_amount": 219}
		response = self.client.post('/api/v1/expenses/search/',data = data, follow_redirects=True)
		self.assert_200(response)
		expenses = json.loads(response.data)
		assert len(expenses['expenses']) == 2

		expense_time = datetime.datetime.now() - datetime.timedelta(days = 4)
		data = {"max_date": int(expense_time.strftime("%s")) * 1000}
		response = self.client.post('/api/v1/expenses/search/',data = data, follow_redirects=True)
		self.assert_200(response)
		expenses = json.loads(response.data)
		assert len(expenses['expenses']) == 1
		

		expense_time = datetime.datetime.now() - datetime.timedelta(days = 1)
		data = {"min_date": int(expense_time.strftime("%s")) * 1000}
		response = self.client.post('/api/v1/expenses/search/',data = data, follow_redirects=True)
		self.assert_200(response)
		expenses = json.loads(response.data)
		assert len(expenses['expenses']) == 1


class TestCommentView(TestCase):

	def test_post(self):
		""" Test Comment Creation"""
		self.login(self.demo_user_details['email'],self.demo_user_details['password'])
		data = dict(
            text = "very expensive",
		)
		response = self.client.post('/api/v1/comment/%s'%self.expense.id, data=data, follow_redirects=True)
		self.assert_200(response)

class TestCommentListView(TestCase):
	
	def test_get(self):
		""" Test Comments List"""
		self.login(self.demo_user_details['email'],self.demo_user_details['password'])
		response = self.client.get('/api/v1/comments/%s'%self.expense.id, follow_redirects=True)
		self.assert_200(response)
		comments = json.loads(response.data)
		assert len(comments) == 1









