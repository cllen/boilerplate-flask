from utils.login import set_user

from ..models import (
    BaseUser as BaseUserModel,
)

from flask import request

from applications import logger

def login(username,password):
    logger.debug('>>>> username: %s password:%s',username,password)
    user = BaseUserModel.query.filter_by(username=username,password=password).first()
    if user:
        if request:
            set_user(user.to_dict())
    else:
        logger.debug('>>>> login failed!')
        return False
    logger.debug('>>>> logined successfully!')
    return user
