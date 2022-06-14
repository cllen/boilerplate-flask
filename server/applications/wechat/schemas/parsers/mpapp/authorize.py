#coding:utf8
# from ......depends_framework.flask.apis import api
from flask_restx import reqparse

Post = reqparse.RequestParser()
Post.add_argument('code', type=str, required=True)

