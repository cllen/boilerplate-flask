#coding:utf8
from flask_restx import Model,fields

User = Model(
	'User',
	{
		'id':fields.String(),
		'nickname':fields.String(),
		'avatar':fields.String(),
		'gender':fields.String(),
	}
)

Post = Model(
	'Single',
	{
		'error_code':fields.Integer(),
		'token':fields.String(),
	},
)

Put = Model(
	'Single',
	{
		'error_code':fields.Integer(),
		'user':fields.Nested(User),
	},
)

List = Model(
	'List',
	{
		'error_code':fields.Integer(),
		'count':fields.Integer(),
		'entries':fields.List(fields.Nested(User)),
	},
)

