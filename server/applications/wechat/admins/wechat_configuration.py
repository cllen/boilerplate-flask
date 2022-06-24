from flask import request, current_app
from flask_admin import expose, BaseView

# from applications.base.utils.flask_admin.view.template import TemplateMixin
from applications.base.utils.flask_admin.login import LoginMixin
from applications.base.utils.flask_admin.query import QueryMixin

import logging
logger = logging.getLogger(__name__)

from applications.wechat import wechat_settings

class WechatConfiguration(LoginMixin,QueryMixin,BaseView):

	html_name = 'admin/wechat_configuration.html'

	@expose('/', methods=['get',])
	def get(self):
		data = wechat_settings
		logger.debug(data.redis_db)
		return self.render(self.html_name, data=data)

	@expose('/', methods=['post',])
	def post(self):
		data = request.form.to_dict()
		data = wechat_settings.update(**data)
		return self.render(self.html_name, data=data)
