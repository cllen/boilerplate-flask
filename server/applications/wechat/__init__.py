
from ctypes import util
import traceback

import logging
logger = logging.getLogger(__name__)

from .utils.settings import WechatSettings

wechat_settings = WechatSettings()

from .admins import (
    WechatConfiguration as WechatConfigurationAdmin,
    WechatUser as WechatUserAdmin,
)
from .models import (
    WechatConfiguration as WechatConfigurationModel,
    WechatUser as WechatUserModel,
)



class Wechat:

    def __init__(self,app=None,admin=None,db=None):
        if None not in [app,admin,db,]:
            self.init_app(app,admin,db)

    def init_app(self,app,admin,db):

        app.wechat = self

        admin.add_view(WechatConfigurationAdmin(name='微信设置',category="微信数据"))
        admin.add_view(WechatUserAdmin(WechatUserModel, db.session, name=u'微信用户',category="微信数据"))

        from .views.v1 import bp as bp_views
        app.register_blueprint(
            bp_views,
            url_prefix='/{}/wechat/'.format(
                app.config['PROJECT_NAME'],
            )
        )

        from .apis.v1 import (
            bp as bp_apis,
        )
        app.register_blueprint(
            bp_apis,
            url_prefix='/{}/api/v1/'.format(
                app.config['PROJECT_NAME'],
            )
        )
