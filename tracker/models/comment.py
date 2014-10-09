# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, not_
from sqlalchemy.orm import relationship
from ..extensions import db
from ..utils import get_current_time, diff
from tracker.serializers import CommentSerializer
from mixins import SaveDeleteMixin,SerializationMixin


class Comment(db.Model,SaveDeleteMixin,SerializationMixin):

    __tablename__ = 'comment'
    __serializer__ = CommentSerializer

    id = Column(db.Integer, primary_key=True)
    user_id = Column(db.Integer,ForeignKey('users.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    expense_id = Column(db.Integer,ForeignKey('expenses.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    text = Column(db.Text, nullable=False)
    pub_date = Column(db.DateTime, default=get_current_time)


    def get_comments_from_user(cls,user,limit=None,offset=0):
        query = cls.query.filter(Comment.user_id == user.id)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        return query.all()

    
