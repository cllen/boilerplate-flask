import abc

import logging
logger = logging.getLogger(__name__)

class BaseSettings:

	# This attribute needs to be override.
	default = {}
	instance = None

	def __init__(self,default={}):

		if default:
			self.default = default

	def __getattr__(self,key):
		self.instance = self._first()
		# logger.debug(self.instance)
		if not self.instance:
			return self.default.get(key,"")
		else:
			return getattr(self.instance,key) or self.default.get(key,"")

	def __setattr__(self,key,value):
		if key in ['default','instance']:
			return super().__setattr__(key,value)
		else:
			self.instance = self._first()
			if self.instance:
				self._update(instance=self.instance,**{key:value})
			else:
				self._save(**{key:value})
			self.instance = self._first()
			return self.instance

	def update(self,**kwargs):
		self.instance = self._first()
		if self.instance is not None:
			self._update(instance=self.instance,**kwargs)
		else:
			self._save(**kwargs)
		self.instance = self._first()
		return self.instance

	@abc.abstractmethod
	def _first(self):
		pass

	@abc.abstractmethod
	def _save(self,**kwargs):
		pass

	@abc.abstractmethod
	def _update(self,instance,**kwargs):
		pass

# class WechatSettings(BaseSettings,metaclass=Singleton):
# default = {
# 	'appid':'xxx',
# 	'app_secret':'xxx',
# 	'app_category':'miniapp',
# 	'mch_id':'xxx',
# 	'mch_secret':'xxx',

# 	'token_secret_key':'xxx',
# 	'token_salt':'xxx',
# 	'token_expiration':60*60*24*7,
	
# 	'redis_db':0,
# 	'redis_host':'xxx',
# 	'redis_port':6379,
# 	'redis_password':'',
# 	'access_token_expiration':60*60*2,
	
# 	'oauth_redirect_url':'xxx',
# 	'post_oauth_redirect_url_default':'xxx',
# 	'oauth_redirect_token_expiration':60*60*24*365,
# 	'mp_token':'xxx',
# }