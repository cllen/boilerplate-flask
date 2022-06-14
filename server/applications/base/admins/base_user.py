from flask_admin.contrib import sqla
from ..utils.flask_admin import LoginMixin
from ..utils.flask_admin import QueryMixin
from ..utils.flask_admin.current_user import CurrentUserMixin

from ..utils.constants import UserRole

class BaseUser(LoginMixin,QueryMixin,CurrentUserMixin,sqla.ModelView):
        
    column_labels = {
        'id':'用户id',
        'username':'用户名',
        'password':'用户密码',
        'role':'用户角色',
        'type':'用户类型'
    }

    column_list = [
        'id',
        'username',
        'password',
        'role',
        'type',
    ]

    form_choices = {'role': [
        (UserRole.USER, UserRole.USER), 
        (UserRole.ADMIN, UserRole.ADMIN), 
    ]}
