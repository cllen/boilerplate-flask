# 标准库
import os
import logging
from utils.log import init_logging
init_logging()

import logging
from utils.log import default_logger
logger = logging.getLogger(default_logger)

# 第三方库
from flask import Flask, Blueprint 
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin 
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_pagedown import PageDown
from flask_moment import Moment
from flask_babelex import Babel


babel = Babel()


# 自己的库

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


# 避免循环导入问题，将部分实例化放到业务代码之前
db = SQLAlchemy()



# 业务代码
from .base import Base
from .wechat import Wechat
from .cms import CMS

from etc import config

from .base.admins import (
	BaseHome as BaseHomeAdmin,
)

# 实例化
base = Base()
wechat = Wechat()
cms = CMS()

migrate = Migrate()
bootstrap = Bootstrap()
pagedown = PageDown()
moment = Moment()

def create_app(config_name='default',import_name=__name__):

	"""app"""
	app = Flask(
		import_name,
		static_url_path='/{}/statics'.format(config[config_name].PROJECT_NAME),
		static_folder='../statics',
		template_folder='../templates'
	)

	"""config"""
	app.config.from_object(config[config_name])
	app_context = app.app_context()
	app_context.push()

	"""修改模板路径"""
	template_path = os.path.abspath(
		os.path.join(
				os.path.dirname(__file__)
			,
			"../",
			'templates',
		)
	)
	bp_template = Blueprint('template',__name__,template_folder=template_path)
	app.register_blueprint(bp_template)


	"""init database"""
	db.init_app(app)
	app.db = db
	# @app.teardown_appcontext
	# def shutdown_session(exception=None):
	# 	db.session.remove()
	# migrate.init_app(app,db)

	# flask-admin
	admin = Admin(
		app,
		name=app.config['PROJECT_CHINESE_NAME'],
		template_mode='bootstrap4',
		base_template='admin/_base.html',
		url='/{}/admin'.format(app.config['PROJECT_NAME']),
		index_view=BaseHomeAdmin(
			name="首页",
			url='/{}/admin'.format(app.config['PROJECT_NAME'])
		)
	)

	"""init modules"""
	bootstrap.init_app(app)
	pagedown.init_app(app)
	moment.init_app(app)
	babel.init_app(app)
	# @babel.localeselector
	# def get_locale():
	# 	from flask import request,session
	# 	if request.args.get('lang'):
	# 		session['lang'] = request.args.get('lang')
	# 	return session.get('lang', 'zh_CN')
	
	"""init applications"""
	base.init_app(app,admin,db)
	wechat.init_app(app,admin,db)
	cms.init_app(app,admin,db)

	app_context.pop()

	return app