#coding:utf8

from ..meta import Singleton
import redis
import traceback

import abc

# log
import logging
logger = logging.getLogger(__name__)


class BaseRedis:

	"""
		这里提供redis最基础的功能
			1. 连接redis
			2. 提供get
			3. 提供set
	"""

	client = None

	@property
	@abc.abstractmethod
	def host(self):
		pass

	@property
	@abc.abstractmethod
	def port(self):
		pass

	@property
	@abc.abstractmethod
	def db(self):
		pass

	@property
	@abc.abstractmethod
	def password(self):
		pass

	def init(self):
		self.try_connect()

	def try_connect(self):
		try:
			self.pool = redis.ConnectionPool(
				host=self.host,
				port=self.port,
				db=self.db,
				password=self.password,
			)
			self.client = redis.StrictRedis(connection_pool=self.pool)
			self.client.ping()
		except redis.exceptions.ConnectionError as e:
			# logger.error(
			# 	'>>>> redis connection error: %s',
			# 	traceback.format_exc(),
			# )
			self.client = None
			raise e

	# 因为使用连接池，所以不需要关闭。
	# def __del__(self):
	# 	pass

	def get(self,key):
		value = self.client.get(key)
		if value is not None:
			value = value.decode('utf8')
			return value
		else:
			return None

	def set(self,key,expires_in,value):
		self.client.setex(key, int(expires_in), value)