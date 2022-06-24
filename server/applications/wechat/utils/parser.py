import traceback
from functools import wraps

from exceptions import JSONException

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from flask import request

def parse_with(parser,exception=JSONException):

	def wrapper1(func):

		@wraps(func)
		def wrapper2(*args,**kwargs):

			try:
				json = parser.parse_args()
			except Exception as e:
				logger.debug('>>>> parse_with')
				# logger.debug(e)
				# logger.debug(traceback.format_exc())
				logger.debug(request.values)
				logger.debug(request.get_json())
				logger.debug(request.args)
				# logger.debug(request.__dict__)
				logger.error(traceback.format_exc())
				raise exception(10003)

			args[0].json = json

			return func(*args, **kwargs)
		return wrapper2
	return wrapper1
