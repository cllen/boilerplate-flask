from sqlalchemy import Column, String, Integer, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship, backref

from ..utils.constants import UserType

from . import db
import logging
logger = logging.getLogger(__name__)


class BaseUser(db.Model):
	__tablename__ = 'base_user'

	id = Column(Integer, primary_key=True)

	# account = Column(Integer, primary_key=True)
	username = Column(String(256))
	password = Column(String(256))
	role = Column(String(256))
	permission = Column(Integer)
	status = Column(String(64))

	@property
	def type(self):
		return UserType.BASE


	def to_dict(self):
		return {
			'id':self.id,
			'username':self.username,
			'password':self.password,
			'role':self.role,
			'permission':self.permission,
			'status':self.status,
		}
