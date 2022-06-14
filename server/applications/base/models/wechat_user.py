from sqlalchemy import Column, String, Integer, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship, backref

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from application import db

from application.base.utils.constants import UserType

class WechatUser(db.Model):
	__tablename__ = 'wechat_user'

	id = Column(Integer, primary_key=True)
	openid = Column(String(200))
	unionid = Column(String(200))
	nickname = Column(String(200))
	gender = Column(String(200))
	language = Column(String(200))
	city = Column(String(200))
	province = Column(String(200))
	country = Column(String(200))
	avatar = Column(String(1000))
	mobile = Column(String(200))
	session_key = Column(String(200))
	category = Column(String(200))

	@property
	def type(self):
		return UserType.WECHAT
