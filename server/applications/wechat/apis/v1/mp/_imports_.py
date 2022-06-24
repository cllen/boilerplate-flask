import logging
import traceback
from flask_restx import Resource

from flask import (
	current_app,
	redirect,
	request,
	session,
)

from itsdangerous import SignatureExpired, BadTimeSignature, BadSignature
from wechatpy.utils import check_signature, random_string
from wechatpy.events import EVENT_TYPES

from .. import api

from ....utils.auth import MpAuth,current_user

from ....utils.parser import parse_with

from exceptions import JSONException

from ....utils.auth import auth

ns = api.namespace('wechat-mp')