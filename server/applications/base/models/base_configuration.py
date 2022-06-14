from sqlalchemy import Column, String, Integer, Boolean
from . import db

class BaseConfiguration(db.Model):
	__tablename__ = 'base_configuration'

	id = Column(Integer, primary_key=True, autoincrement=True)

	redis_db = Column(String(256))
	redis_host = Column(String(256))
	redis_port = Column(Integer)
	redis_password = Column(String(256))

	def to_dict(self):
		return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
