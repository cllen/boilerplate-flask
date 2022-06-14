# -*- coding: utf-8 -*-

# from marshmallow import fields

# from wechat_utils.parser import ParserBase

# class Verification(ParserBase):
# 	signature = fields.Str()
# 	timestamp = fields.Integer()
# 	nonce = fields.Str()
# 	echostr = fields.Str()


#coding:utf8
# from ......depends_framework.flask.apis import api
from flask_restx import reqparse

Verification = reqparse.RequestParser()
Verification.add_argument('signature', type=str, required=True)
Verification.add_argument('timestamp', type=int, required=True)
Verification.add_argument('nonce', type=str, required=True)
Verification.add_argument('echostr', type=str, required=True)
