
from ctypes import util
import traceback

import logging
logger = logging.getLogger(__name__)

from .utils.settings import Settings
from .utils.redis import Redis

# # 避免循环导入
settings = Settings()
redis = Redis()

from .admins import (
	BaseConfiguration as BaseConfigurationAdmin,
	BaseUser as BaseUserAdmin,
)
from .models import (
	BaseConfiguration as BaseConfigurationModel,
	BaseUser as BaseUserModel,
)

class Base:

	def __init__(self,app=None,admin=None,db=None):
		if None not in [app,admin,db,]:
			self.init_app(app,admin,db)

	def init_app(self,app,admin,db):

		app.base = self

		admin.add_view(BaseConfigurationAdmin(name='基本设置',category="基本数据"))
		admin.add_view(BaseUserAdmin(BaseUserModel, db.session, name=u'基本用户',category="基本数据"))

		from .views import bp as bp_views
		app.register_blueprint(
			bp_views,
			url_prefix='/{}/base/'.format(
				app.config['PROJECT_NAME'],
			)
		)
		from .apis.v1 import bp as bp_apis
		app.register_blueprint(
			bp_apis,
			url_prefix='/{}/api/v1/'.format(
				app.config['PROJECT_NAME'],
			)
		)

		# from .. import miniorm
		# settings.init(miniorm,BaseConfigurationModel)
		# self.settings=settings

		try:
			redis.init(settings)
		except Exception as e:
			logger.warning(traceback.format_exc())
		self.redis=redis
