from functools import wraps

from flask import (
    session,request,Response,render_template,current_app,
    redirect,url_for,
)
from werkzeug.local import LocalProxy
from werkzeug.exceptions import HTTPException
from werkzeug.http import parse_authorization_header

import logging

logger = logging.getLogger(__name__)

current_user = LocalProxy(lambda: _get_user())



def _get_user():
    return session.get('user') if session.get('user') else None

def set_user(user):
    session['user'] = user
    return True

def parse_username_password():
    # logger.debug('>>>> get_username_password')
    FIELD_KEY = 'HTTP_AUTHORIZATION'
    field_value = request.environ.get(FIELD_KEY)
    # logger.error(field_value)
    if not field_value:
        return False,False

    authorization = parse_authorization_header(field_value)
    if not authorization:
        return False,False
    # logger.debug("{},{}".format(authorization.username,authorization.password))
    return authorization.username,authorization.password

def _make_login_required_response(realm=''):
    return 401,{'WWW-Authenticate': 'Basic realm="%s"' % realm}

def make_login_required_response():
    status,header = _make_login_required_response()
    return Response(
        status=status,
        headers=header,
    )

def make_login_required_exception():
    return HTTPException(response=make_login_required_response())

def view_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user:
            # return make_login_required_response()
            return redirect(url_for('base-views.login'))
        return func(*args,**kwargs)
    return wrapper

def api_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user:
            raise 
        return func(*args,**kwargs)
    return wrapper