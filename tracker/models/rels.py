# This resolves circular dependency issue

from tracker.extensions import db
from tracker.models import User, Expense, Comment

def make_relation(cls_a, prop_name, cls_b, backref=None, id_prop_name=None):
    if id_prop_name is None:
        id_prop_name = prop_name + '_id'

    if not hasattr(cls_a, id_prop_name):
        raise RuntimeError("%s has no %s" % (cls_a, id_prop_name))

    foreign_keys = [getattr(cls_a, id_prop_name)]
    
    if backref:
        rel = db.relationship(
            cls_b, foreign_keys=foreign_keys, backref=backref)
    else:
        rel = db.relationship(cls_b, foreign_keys=foreign_keys)
    
    if not hasattr(cls_a, prop_name):
        setattr(cls_a, prop_name, rel)

def make_relations():
    make_relation(Expense, 'user', User, 'expenses','user_id')
    make_relation(Comment, 'expense',Expense, 'comments','expense_id')
    make_relation(Comment, 'user',User , 'comments','user_id')