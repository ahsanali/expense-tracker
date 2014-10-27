# -*- coding: utf-8 -*-
from flask.ext.testing import TestCase as Base

from tracker import create_app
from tracker.models import User, Expense, Comment
from tracker.config import TestConfig
from tracker.extensions import db
from flask.ext.login import login_user
import datetime


class TestCase(Base):
    """Base TestClass for your application."""

    def create_app(self):
        """Create and return a testing flask app."""

        app = create_app(TestConfig)
        # self.twill = Twill(app, port=3000)
        return app

    def init_data(self):

        self.demo_user_details = dict(
            name=u'test',
            email=u'test@example.com',
            password=u'123456',
            )
        self.demo_user = User(
                **self.demo_user_details
                )

        login_user(self.demo_user)

        self.expense_details = dict(
            description = "Mangoes",
            expense_time = int(datetime.datetime.now().strftime("%s"))*1000,
            amount = 12.00,
            user = self.demo_user
            )
        self.expense = Expense(
            **self.expense_details
            )

        self.comment_details = dict(
            text = "very expensive",
            user = self.demo_user,
            expense = self.expense
            )

        self.comment = Comment(**self.comment_details)

        db.session.add(self.comment)
        db.session.add(self.expense)
        db.session.add(self.demo_user)

        db.session.commit()

    def setUp(self):
        """Reset all tables before testing."""

        db.create_all()
        self.init_data()

    def tearDown(self):
        """Clean db session and drop all tables."""

        db.drop_all()

    def login(self, username, password):
        data = {
            'email': username,
            'password': password,
        }
        response = self.client.post('/api/v1/session', data=data, follow_redirects=True)
        self.assert_200(response)
        return response

    def _logout(self):
        response = self.client.get('/api/v1/logout')
        self.assert_200(response)

    def _test_get_request(self, endpoint, template=None):
        response = self.client.get(endpoint)
        self.assert_200(response)
        if template:
            self.assertTemplateUsed(name=template)
        return response

    def assert_201(self,response):
        assert response.status_code == 201

    def assert_422(self,response):
        assert response.status_code == 422
