#coding:utf8
from flask_restx import fields
from ....apis.v1 import api
User = api.model(
	'User',
	{
		'id':fields.String(),
		'nickname':fields.String(),
		'avatar':fields.String(),
		'gender':fields.String(),
	}
)

Post = api.model(
	'Single',
	{
		'error_code':fields.Integer(),
		'token':fields.String(),
	},
)

Put = api.model(
	'Single',
	{
		'error_code':fields.Integer(),
		'user':fields.Nested(User),
	},
)

List = api.model(
	'List',
	{
		'error_code':fields.Integer(),
		'count':fields.Integer(),
		'entries':fields.List(fields.Nested(User)),
	},
)

