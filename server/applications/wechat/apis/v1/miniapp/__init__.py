#coding:utf8
"""
	微信网页与微信小程序授权的区别是：

	1. 微信网页是oauth2的client角色
	2. 而微信小程序是oauth2的client的第六步开始（我的统一登录的笔记）
"""

from flask import Blueprint
from flask_restx import Api

bp = Blueprint('miniapp-api',__name__)
api = Api(bp)

from . import (
	user,
)