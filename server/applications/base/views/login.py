from ._imports_ import *

from utils.login import (
    parse_username_password,
    make_login_required_response,
    _make_login_required_response,
    set_user,
)
from ..services import login

from flask import session,make_response

import logging
logger = logging.getLogger(__name__)

@bp.route('/login',methods=('GET',),endpoint='login')
def _login():
    logger.debug('>>>> login')
    if not session.get('referrer') and \
            hasattr(request,'referrer') and \
            request.referrer and \
            'logout' not in request.referrer and \
            'login' not in request.referrer:
        session['referrer'] = request.referrer
    username,password = parse_username_password()
    if not username or not password:
        return make_login_required_response()
    user = login(username,password)
    if not user:
        return make_login_required_response()
    set_user(user.to_dict())
    if session.get('referrer'):
        referrer = session.get('referrer')
        session['referrer'] = None
        # return redirect(referrer)
    return redirect(url_for('vocabulary-views.home'))


@bp.route('/logout',methods=('GET',))
def logout():
    set_user(None)

    # 4. 重定向。
    # return redirect(current_app.urls['home_url'])
    # return make_login_required_response()
    http_code,header = _make_login_required_response()
    response = make_response(
        render_template('home/logout.html'),
        http_code
    )
    # response.headers.update(header)
    return response