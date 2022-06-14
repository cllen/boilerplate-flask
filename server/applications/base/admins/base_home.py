import logging
from flask_admin import AdminIndexView,expose
from flask import current_app

from ..utils.flask_admin.query import QueryMixin
from ..utils.flask_admin.login import LoginMixin
from utils.login import current_user
from ..utils.flask_admin.current_user import CurrentUserMixin
from utils.login import view_login_required,current_user

from flask import redirect,url_for

logger = logging.getLogger(__name__)

class BaseHome(QueryMixin,CurrentUserMixin,AdminIndexView):
	@expose('/')
	def get(self):
		return self.render('admin/home.html')

