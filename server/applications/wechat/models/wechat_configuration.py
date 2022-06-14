from sqlalchemy import Column, String, Integer, Boolean
from applications import db

class WechatConfiguration(db.Model):
	__tablename__ = 'wechat_configuration'

	id = Column(Integer, primary_key=True)
	appid = Column(String(200))
	app_secret = Column(String(200))
	app_category = Column(String(200))
	mch_id = Column(String(200))
	mch_secret = Column(String(200))
	token_secret_key = Column(String(200))
	token_salt = Column(String(200))
	token_expiration = Column(Integer)
	redis_db = Column(String(200))
	redis_host = Column(String(200))
	redis_port = Column(Integer)
	redis_password = Column(String(200))
	access_token_expiration = Column(Integer)

	oauth_callback_url = Column(String(200))
	post_oauth_beforeauthorize_url_default = Column(String(200))
	oauth_beforeauthorize_token_expiration = Column(Integer)
	mp_token = Column(String(200))

	def to_dict(self):
		return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

# class Configuration(BaseConfiguration):
# 	pass
