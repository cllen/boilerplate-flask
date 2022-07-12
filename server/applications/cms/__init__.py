
from ctypes import util
import traceback

import logging
logger = logging.getLogger(__name__)



from .admins import (
    Article as ArticleAdmin,
)
from .models import (
    Article as ArticleModel,
)

class CMS:

    def __init__(self,app=None,admin=None,db=None):
        if None not in [app,admin,db,]:
            self.init_app(app,admin,db)

    def init_app(self,app,admin,db):

        app.cms = self

        admin.add_view(ArticleAdmin(ArticleModel, db.session, name=u'文章管理',category="内容管理系统"))
        from .apis.v1 import bp as bp_apis
        app.register_blueprint(
            bp_apis,
            url_prefix='/{}/api/v1/cms/'.format(
                app.config['PROJECT_NAME'],
            )
        )
