from flask import current_app

import logging

from utils.login import (
    parse_username_password,
    make_login_required_response,
    make_login_required_exception,
    set_user,
    current_user,
)

from ...services.login import login

logger = logging.getLogger(__name__)

class LoginMixin:

    def is_accessible(self):

        username,password = parse_username_password()
        logger.debug('>>>> is_accessible')
        logger.debug(username)
        logger.debug(password)
        if current_user:
            return True
        if not username or not password:
            raise make_login_required_exception()
        user = login(username,password)
        if not user:
            raise make_login_required_exception()
        set_user(user.to_dict())
        return True
    
    def inaccessible_callback(self, name, **kwargs):
        return make_login_required_response()
