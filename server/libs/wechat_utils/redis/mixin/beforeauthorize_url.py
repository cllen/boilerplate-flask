#coding:utf8
import traceback
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from abc import ABCMeta, abstractmethod

from ...constants import Keys



class BeforeAuthorizeUrlMixin:

	"""
		这里提供公众号的功能
			1. 提供登录成功后的重定向，原则上是返回到授权登录前的页面
	"""

	@property
	@abstractmethod
	def oauth_beforeauthorize_token_expiration(self):
		pass

	def persist_beforeauthorize(self, token, url):
		try:
			key = Keys.oauth_redirect_token.format(token)
			self.base_redis.set(key, self.oauth_beforeauthorize_token_expiration, url)
		except:
			logger.error(
				'Error while persisting oauth redirect token. token: %s url: %s Err: %s',
				token,
				url,
				traceback.format_exc(),
			)
			return False
		else:
			return True

	def retrieve_beforeauthorize(self, token):
		try:
			key = Keys.oauth_redirect_token.format(token)
			url = self.base_redis.get(key)
		except:
			logger.error(
				'Error while retrieving oauth redirect url. token: %s Err: %s',
				token,
				traceback.format_exc(),
			)
			return None
		else:
			return url
