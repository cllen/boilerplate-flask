# -*- coding: utf-8 -*-

from werkzeug.exceptions import HTTPException

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import traceback
import json

from flask import request

class AppException(HTTPException):
	co_msg_mapping = {}

	def __init__(self, 
		error_code, 
		http_code=None,
		error_message=None,
		error_detail=None, 
		params={},
		return_data={},
		error_html=""
	):
		super().__init__(description=traceback.format_exc())

		self.error_code = error_code
		# code的命名是HTTPException规定的，不要修改。
		self.code = http_code or self.co_msg_mapping.get(error_code)['http_code']
		self.error_message = error_message or self.co_msg_mapping.get(error_code)['error_message']
		self.error_detail = error_detail or traceback.format_exc()
		# self.params = params or {
		# 	'values':dict(request.values),
		# 	'json':request.get_json(),
		# }
		self.params = params
		self.return_data = return_data
		self.error_html = error_html

		self.data = {
			'http_code':self.code,
			'error_code': self.error_code,
			'error_message': self.error_message,
			'error_detail':self.error_detail,
			'params':self.params,
			'return_data':self.return_data,
			'error_html':self.error_html
		}

	def __repr__(self):
		return json.dumps(self.data)

