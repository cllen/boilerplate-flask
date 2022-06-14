import traceback
import logging
logger = logging.getLogger(__name__)

from libs.redis import BaseRedis
from libs.meta import Singleton

class Redis(BaseRedis, metaclass=Singleton):

	def __init__(self,settings=None):
		if settings != None:
			self.init(settings)

	def init(self,settings):
		self.settings = settings
		super().init()

	def try_connect(self):
		try:
			super().try_connect()
		except Exception as e:
			logger.warning(traceback.format_exc())

	@property
	def host(self):
		return self.settings.redis_host

	@property
	def port(self):
		return self.settings.redis_port

	@property
	def db(self):
		return self.settings.redis_db

	@property
	def password(self):
		return self.settings.redis_password