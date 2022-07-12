from utils.login import set_user

from ..models import (
    BaseUser as BaseUserModel,
)

from flask import request

import logging
logger = logging.getLogger(__name__)

def login(username,password):
    logger.debug('>>>> login')
    user = BaseUserModel.query.filter_by(username=username,password=password).first()
    if user:
        if request:
            set_user(user.to_dict())
    else:
        logger.debug('>>>> login failed!')
        return False
    logger.debug('>>>> login successfully!')
    return user
