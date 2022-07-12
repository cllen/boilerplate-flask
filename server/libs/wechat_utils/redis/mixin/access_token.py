import abc
from abc import ABCMeta, abstractmethod
import requests
from ...constants import Keys

class AccessTokenMixin:

	@property
	@abc.abstractmethod
	def appid(self):
		pass

	@property
	@abc.abstractmethod
	def app_secret(self):
		pass

	@property
	def access_token(self):

		def _get_access_token_from_tencent(appid,app_secret):
			url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}".format(
				appid=appid,
				appsecret=app_secret,
			)
			response = requests.get(url)
			return response.json()['access_token'],response.json()['expires_in']

		# get access_token from redis
		access_token = self.base_redis.get(Keys.access_token)
		
		if access_token is None:

			# get access_token from tencent
			access_token,expires_in = _get_access_token_from_tencent(self.appid,self.app_secret)

			# save access_token to redis
			self.base_redis.set(Keys.access_token,expires_in,access_token)
		return access_token