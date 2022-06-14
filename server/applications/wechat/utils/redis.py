from libs.wechat_utils.redis import (
	BaseWechatRedis,
	AccessTokenMixin,
	BeforeAuthorizeUrlMixin,
)

from libs.meta import Singleton

from applications.base import redis


class WechatRedis(
	BaseWechatRedis,
	AccessTokenMixin, 
	BeforeAuthorizeUrlMixin,
	metaclass=Singleton
):
	@property
	def base_redis(self):
		return redis

	@property
	def appid(self):
		return self.wechat_settings.appid

	@property
	def app_secret(self):
		return self.wechat_settings.app_secret

	@property
	def oauth_beforeauthorize_token_expiration(self):
		return self.wechat_settings.oauth_beforeauthorize_token_expiration