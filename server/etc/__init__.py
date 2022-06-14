import os
import abc
import socket
basedir = os.path.abspath(os.getcwd())

config_path = os.path.join(
	#os.path.dirname(				# 1code
		os.path.dirname(			# vocabulary-flask
			os.path.dirname( 		# server
				os.path.dirname( 	# etc
					__file__
				)
			)
		# )
	),
	'config.conf'
)

from configparser import ConfigParser

parser = ConfigParser()
with open(config_path,encoding='utf-8') as stream:
	parser.read_string("[top]\n" + stream.read())  # This line does the trick.

# project
project_name = parser.get('top', 'project_name')
project_chinese_name = parser.get('top', 'project_chinese_name')

# db
db_host = parser.get('top', 'db_host')
db_port = parser.get('top', 'db_port')
db_username = parser.get('top', 'db_username')
db_password = parser.get('top', 'db_password')

# service
domain = parser.get('top', 'domain')

# 这几个用上
gunicorn_ip = parser.get('top', 'gunicorn_ip')
gunicorn_port = parser.get('top', 'gunicorn_port')

admin_username = parser.get('top', 'admin_username')
admin_password = parser.get('top', 'admin_password')


class SystemConfig:

	"""
		这里的配置是给开发者修改的。

		存放了如文件路径等参数。
	"""

	# flask-admin-image,video,file
	UPLOADS_PATH = os.path.join(
		os.path.abspath(os.getcwd()), 
		"static",
		"uploads"
	)

	def get_FILE_UPLOAD_URL(self):
		return "".join([
			self.DOMAIN,
			"/",
			self.PROJECT_NAME,
			"/",
			"static",
			"/"
			"uploads",
			"/"
		])

	def get_FILE_DOWNLOAD_URL(self):
		return self.get_FILE_UPLOAD_URL()

class BaseConfig(SystemConfig):

	"""
		这里的配置是给运维修改的。

		存放了：数据库、管理后台账号密码等参数。
	"""

	# applications
	SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxx'
	
	# sqlalchemy
	SQLALCHEMY_TRACK_MODIFICATIONS = True

	PROJECT_NAME = project_name # authorization and resource

	PROJECT_CHINESE_NAME = project_chinese_name

	# admin
	ADMIN_USERNAME = admin_username
	ADMIN_PASSWORD = admin_password

	DOMAIN = domain

	BUNDLE_ERRORS = True

	BOOTSTRAP_SERVE_LOCAL = True


class DevelopmentConfig(BaseConfig):

	

	# sqlalchemy
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, project_name+'-dev.sqlite')


class TestingConfig(BaseConfig):

	# sqlalchemy
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, project_name+'-testing.sqlite')

class ProductionConfig(BaseConfig):

	SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://{user}:{password}@{server}/{database}'.format(
		user='db_user', 
		password='db_password', 
		server='db_host:db_port',
		database='db_name')

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}