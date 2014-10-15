from sqlalchemy import Column, types
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

from tracker.extensions import db
from tracker.utils import get_current_time, SEX_TYPE, STRING_LEN
# from .constants import USER, USER_ROLE, ADMIN, INACTIVE, USER_STATUS
from flask.ext.login import UserMixin
import pdb
from mixins import SaveDeleteMixin,SerializationMixin
from tracker.serializers import UserSerializer


class User(db.Model, UserMixin,SaveDeleteMixin,SerializationMixin):

    __tablename__ = 'users'
    __serializer__ = UserSerializer

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(STRING_LEN), nullable=False, unique=True)
    email = Column(db.String(STRING_LEN), nullable=False, unique=True)
    # activation_key = Column(db.String(STRING_LEN))
    created_time = Column(db.DateTime, default=get_current_time)
    age = Column(db.Integer)
    phone = Column(db.String(STRING_LEN))
    sex_code = db.Column(db.Integer)
    _password = Column('password', db.String(STRING_LEN), nullable=False)

    
    @property
    def sex(self):
        return SEX_TYPE.get(self.sex_code)


    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)
    
    # Hide password encryption by exposing password field only.
    password = db.synonym('_password',
                          descriptor=property(_get_password,
                                              _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    # def reset_password(self):
    #     self.activation_key = str(uuid4())
    #     db.session.add(self)
    #     db.session.commit()

    # def change_password(self):
    #     self.password = self.password.data
    #     self.activation_key = None
    #     db.session.add(self)
    #     db.session.commit()


# ================================================================
    # Class methods

    @classmethod
    def authenticate(cls, login, password):
        # pdb.set_trace()
        user = cls.query.filter(User.email == login).first()
        print user
        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated

    # @classmethod
    # def search(cls, keywords):
    #     criteria = []
    #     for keyword in keywords.split():
    #         keyword = '%' + keyword + '%'
    #         criteria.append(db.or_(
    #             User.name.ilike(keyword),
    #             User.email.ilike(keyword),
    #         ))
    #     q = reduce(db.and_, criteria)
    #     return cls.query.filter(q)

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first_or_404()

    def check_name(self, name):
        return User.query.filter(db.and_(User.name == name, User.email != self.id)).count() == 0
