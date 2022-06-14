from flask import request, current_app
from flask_admin import expose, BaseView

from ..utils.flask_admin.template import TemplateMixin
from ..utils.flask_admin.login import LoginMixin
from ..utils.flask_admin.query import QueryMixin
from ..utils.flask_admin.current_user import CurrentUserMixin

import logging

from ..utils.settings import Settings

settings = Settings()

logger = logging.getLogger(__name__)

class BaseConfiguration(LoginMixin,QueryMixin,CurrentUserMixin,BaseView):
        
    html_name = 'admin/base_configuration.html'

    @expose('/', methods=['get',])
    def get(self):
        data = settings
        return self.render(self.html_name, data=data)

    @expose('/', methods=['post',])
    def post(self):
        data = request.form.to_dict()
        data = settings.update(**data)
        return self.render(self.html_name, data=data)

