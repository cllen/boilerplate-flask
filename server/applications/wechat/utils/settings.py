from libs.meta import Singleton
from libs.settings import BaseSettings
from applications import db

from ..models import (
	WechatConfiguration as WechatConfigurationModel,
)

class WechatSettings(BaseSettings,metaclass=Singleton):
	default={
		'appid':'xxx',
		'app_secret':'xxx',
		'token_secret_key':'xxx',
		'token_salt':'xxx',
		'token_expiration':99999,
		'access_token_expiration':99999,

		'mch_id':'xxx',
		'mch_secret':'xxx',

		'oauth_callback_url':'http://ip:port/xxx/wechat-mp/api/v1/calback',
		'post_oauth_beforeauthorize_url_default':'http://ip:port/xxx/wechat-mp/view/index',
		'oauth_beforeauthorize_token_expiration':99999,
		'mp_token':'???',
	}

	def _first(self):
		return db.session.query(WechatConfigurationModel).first()

	def _save(self,**kwargs):
		instance = WechatConfigurationModel(**kwargs)
		self.db.session.add(instance)
		self.db.session.commit()
		return instance

	def _update(self,instance,**kwargs):
		for key,value in kwargs.items():
			setattr(instance,key,value)
		self.db.session.commit()
		return instance