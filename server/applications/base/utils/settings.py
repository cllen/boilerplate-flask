from libs.settings import BaseSettings
from libs.meta import Singleton
from application import db
from ..models import (
	BaseConfiguration as BaseConfigurationModel,
)
class Settings(BaseSettings,metaclass=Singleton):
	default = {
		'redis_db':0,
		'redis_host':'localhost',
		'redis_port':6379,
		'redis_password':'',
	}

	def _first(self):
		return db.session.query(BaseConfigurationModel).first()

	def _save(self,**kwargs):
		instance = BaseConfigurationModel(**kwargs)
		self.db.session.add(instance)
		self.db.session.commit()
		return instance

	def _update(self,instance,**kwargs):
		for key,value in kwargs.items():
			setattr(instance,key,value)
		self.db.session.commit()
		return instance