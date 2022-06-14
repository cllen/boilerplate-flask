#coding:utf8

from ..meta import Singleton
import redis
import traceback

import abc

# log
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

"""""""""""""""""""""""""""

Client
======
* author	:	黄旭辉
* update	:	２０１９年０６月１５日１８：０５：０２


what
----
A class-based redis client

why
---
* Singleton	:	new one anywhere anytime you want,it will make itself's connention singleton.
* extend	:	you can inherit it and add some functions you want.

how-usage
---------

using it straightly is not a good idea.
you should use it like:

```python
class MyClient(object):
	def __new__(self):
		return Client(
			host=config.host,
			port=config.port,
			db=config.db,
			password=config.password)

myclient = MyClient()
myclient.client.set(name='hello', value='world', ex=60*1, px=None, nx=False, xx=False')
myclient.get('hello')
```

"""""""""""""""""""""""""""


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
			logger.error(
				'redis connection error: %s',
				traceback.format_exc(),
			)
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