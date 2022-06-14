#coding:utf8
# from ......depends_framework.flask.apis import api
from flask_restx import reqparse

#Post = api.parser()
Post = reqparse.RequestParser()
Post.add_argument('code', type=str, required=True)

Put = reqparse.RequestParser()
Put.add_argument('authorization', type=str, required=True, location='headers')
Put.add_argument('iv', type=str, required=True)
Put.add_argument('encrypted_data', type=str, required=True)
