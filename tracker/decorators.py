from functools import wraps
from flask import current_app
from flask.ext.login import current_user
def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated():
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view