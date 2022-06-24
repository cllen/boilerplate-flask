from flask_admin.contrib import sqla
from applications.base.utils.flask_admin.login import LoginMixin
from applications.base.utils.flask_admin.query import QueryMixin
from flask_admin import form
from markupsafe import Markup

class WechatUser(LoginMixin,QueryMixin,sqla.ModelView):

	def _list_thumbnail(view, context, model, name):
		if not model.avatar:
			return ''

		return Markup('<img src="%s" style="height:40px;width:40px">' % model.avatar)

	column_labels = {
		'id':'用户id',
		'nickname':'昵称',
	}

	column_list = [
		'id',
		'nickname',
		'avatar',
		'mobile',
	]

	column_formatters = {
        'avatar': _list_thumbnail
    }



