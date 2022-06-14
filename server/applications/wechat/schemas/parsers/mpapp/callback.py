#coding:utf8
from flask_restx import reqparse

Get = reqparse.RequestParser()
Get.add_argument('code', type=str, required=True)
Get.add_argument('state', type=str, required=True)
