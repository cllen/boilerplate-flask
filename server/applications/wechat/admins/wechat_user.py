from flask_admin.contrib import sqla
from applications.base.utils.flask_admin.view.login_basichttp import LoginMixin
from applications.base.utils.flask_admin.view.query import QueryMixin

class WechatUser(LoginMixin,QueryMixin,sqla.ModelView):
	
	column_labels = {
		'id':'用户id',
	}

	column_list = [
		'id',
	]
