from sqlalchemy import Column
from tracker.extensions import db
from tracker.utils import get_current_time
from tracker.serializers import ExpenseSerializer
from flask.ext.login import current_user
from mixins import SaveDeleteMixin,SerializationMixin
#  date, time, description, amount, comment

class Expense(db.Model,SaveDeleteMixin,SerializationMixin):

    __tablename__ = 'expenses'
    __serializer__ = ExpenseSerializer

    id = Column(db.Integer, primary_key=True)
    description = Column(db.Text, nullable=False)
    created_time = Column(db.DateTime, default=get_current_time)
    expense_time = Column(db.BIGINT,nullable=False)
    amount = Column(db.FLOAT)
    user_id = Column(db.Integer, db.ForeignKey("users.id"))

    @classmethod
    def get_user_expenses(cls):
    	return cls.query.filter(Expense.user_id == current_user.id).all()

    @classmethod
    def get_week_expenses(cls,start,end):
        return cls.query.filter(Expense.user_id == current_user.id).\
                            filter(Expense.expense_time >= start).\
                            filter(Expense.expense_time <= end).\
                            order_by(Expense.created_time)\
                            .all()

    @classmethod
    def get_comments(cls,expense_id):
        expense = cls.query.get_or_404(expense_id);
        return expense.comments
