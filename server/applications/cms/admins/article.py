import logging
logger = logging.getLogger(__name__)

from flask_admin.contrib import sqla
from ...base.utils.flask_admin import LoginMixin
from ...base.utils.flask_admin import QueryMixin
from ...base.utils.flask_admin.current_user import CurrentUserMixin

from flask_admin import form
from markupsafe import Markup
from flask import url_for
import os.path as op
import datetime
import ast

from ..utils.flask_admin.form_upload import MultipleImageUploadField


from sqlalchemy.event import listens_for
import ast
import os
import os.path as op
from flask_admin import form

from ..models import Article

uploads_path = op.join(
    op.dirname(                         # server
        op.dirname(                     # applications
            op.dirname(                 # cms
                op.dirname(__file__)    # admins
            )
        )
    ), 'statics', 'uploads')

def prefix_name(obj, file_data):
    while True:
        now = datetime.datetime.now()
        str_now = str(now).replace(':','..').replace(' ','_')
        if not op.isfile(str_now):
            return str_now


@listens_for(Article, "after_delete")
def after_images(mapper, connection, target):
    # if target.files:
    #     files = ast.literal_eval(target.files)
    #     for file in files:
    #         try:
    #             os.remove(op.join(uploads_path, file))
    #         except OSError:
    #             logger.debug(e)
    #         except Exception as e:
    #             logger.debug(e)

    if target.images:
        images = ast.literal_eval(target.images)
        for image in images:
            try:
                logger.debug(op.join(uploads_path, image))
                os.remove(op.join(uploads_path, image))
            except OSError:
                logger.debug(e)
            except Exception as e:
                logger.debug(e)

            try:
                os.remove(op.join(uploads_path, form.thumbgen_filename(image)))
            except OSError:
                pass
            

class Article(LoginMixin,QueryMixin,CurrentUserMixin,sqla.ModelView):

    column_labels = {
        'id':'用户id',
        'image':'单个图片',
        'images':'多个图片',
        'video':'单个视频',
        'videos':'多个视频'
    }

    column_list = [
        'id',
        'image',
        'images',
        'video',
        'videos',
    ]

    def _list_thumbnail(view, context, model, name):
        if not model.image:
            return ''

        return Markup('<img src="%s">' % url_for('static',
            filename="uploads/"+form.thumbgen_filename(model.image)))


    def _list_thumbnails(view, context, model, name):

        if not model.images:
            return ""

        def gen_img(filename):
            return '<img src="{}">'.format(url_for('static', 
                filename="uploads/"+ form.thumbgen_filename(filename)))

        return Markup("<br />".join([gen_img(image) for image in ast.literal_eval(model.images)]))
        
    column_formatters = {
        'image': _list_thumbnail,
        'images': _list_thumbnails
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'image': form.ImageUploadField('Image',
            base_path=uploads_path,
            url_relative_path='uploads/',
            thumbnail_size=(100, 100, True),
            namegen=prefix_name,
        ),
        "images": MultipleImageUploadField("Images",
            base_path=uploads_path,
            url_relative_path='uploads/',
            thumbnail_size=(100, 100, True),
            namegen=prefix_name,
        )
    }