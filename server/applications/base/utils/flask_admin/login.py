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

logger = logging.getLogger('boilerplate')


class LoginMixin:

    def is_accessible(self):

        username,password = parse_username_password()
        logger.debug('>>>> self:%s username:%s password:%s',self.__class__.__name__,username,password)
        
        # 要注销掉这句，不然不能退出登录。
        # 因为testclient没有session，所以unittest没有测试出来这个错误，后期还是要写selenium。
        # if current_user:
        #     return True

        if not username or not password:
            logger.debug('>>>> not username or not password!')
            raise make_login_required_exception()
        user = login(username,password)
        if not user:
            logger.debug('>>>> not user!')
            raise make_login_required_exception()
        set_user(user.to_dict())
        return True
    def inaccessible_callback(self, name, **kwargs):
        return make_login_required_response()
