from flask import request


from functools import wraps

from .auth import current_user

import logging

from exceptions import JSONException,HTMLException

from libs.meta import Singleton

from loguru import logger
import sys

from rich.logging import RichHandler

handler = RichHandler(
	rich_tracebacks=True,
)

logger.remove()
logger.add(
	handler,
	format=lambda _: "{message}",
	backtrace=False,
	diagnose=False,
	level="ERROR",
)

logger.add(
	sys.stdout,
	colorize=True, 
	format="<green>{time:YYYY-MM-DD}</green><blue> at </blue><green>{time:HH:mm:ss}</green> \
	| <level>{level}</level> | <level>{message}</level> |",
	# backtrace=False,
	# diagnose=False,
	level='INFO'
)

logger.add(
	"log/{time:YYYY-MM-DD}.log",
	format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message} |",
	rotation="00:00",
	retention="7 days",
	compression="zip",
	backtrace=False,
	diagnose=False,
	# enqueue=True
)

class Logging(object, metaclass=Singleton):

	def __init__(self,yaml_file="etc/logging_config.yml"):
		if yaml_file != None:
			self.init(yaml_file)

	def init(self,yaml_file):
		import logging.config

		import yaml

		with open(yaml_file, "r", encoding="utf8") as f:
			logging_config = yaml.safe_load(f)
		logging.config.dictConfig(logging_config)
		self.logger = logging.getLogger('app')

	def getLogger(self):
		return self.logger

log = Logging()
# logger = log.getLogger()


def catch_exception(default_exception=JSONException):

	def wrapper1(func):

		@wraps(func)
		def wrapper2(*args,**kwargs):

			try:
				
				message = "{method} | {url} | userid:'{userid}' | token:'{token}' | params:{params}".format(
					userid=current_user.id if current_user else 'x',
					method=request.method,
					url=request.path,
					params=dict(request.get_json()) or {},
					token=request.environ.get('HTTP_TOKEN'),
				)

				logger.info(message)

				returns = func(*args,**kwargs)

				return returns

			except JSONException as e:
				logger.exception(e)
				raise e
			except HTMLException as e:
				logger.exception(e)
				raise e
			except Exception as e:
				logger.exception(e)
				raise default_exception(10001)

		return wrapper2

	return wrapper1
