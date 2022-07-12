from flask_admin._compat import string_types, urljoin
from wtforms.widgets import html_params
from markupsafe import Markup
from flask_admin.helpers import get_url
try:
    from wtforms.fields.core import _unset_value as unset_value
except ImportError:
    from wtforms.utils import unset_value
import ast
from PIL import Image
from wtforms.validators import ValidationError

from flask_admin.form import ImageUploadField

import os.path as op

import logging
logger = logging.getLogger(__name__)

class MultipleImageUploadInput(object):

    """
        Render a image input chooser field which you can choose multiple images.
        You can customize `empty_template` and `data_template` members to customize
        look and feel.
    """

    empty_template = ('<input %(file)s multiple>')

    data_template = ('<div class="image-thumbnail">'
                     '    %(images)s'
                     '</div>'
                     '<input %(file)s multiple>')

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.name)

        args = {"file": html_params(type="file", **kwargs)}

        if field.data and isinstance(field.data, string_types):

            attributes = self.get_attributes(field)
            # import logging
            # logger = logging.getLogger(__name__)
            # for attribute in attributes:
            #     logger.debug(attribute[0].split('/')[-1])
            args["images"] = "&emsp;".join(["<img src='{}' /><input type='checkbox' name='_{}-delete'>Delete</input>"
                                           .format(attribute[0], attribute[0].split('/')[-1].replace('_thumb','')) for attribute in attributes])
            # logger.debug(args['images'])

            template = self.data_template

        else:
            template = self.empty_template

        return Markup(template % args)

    def get_attributes(self, field):

        for item in ast.literal_eval(field.data):

            filename = item

            if field.thumbnail_size:
                filename = field.thumbnail_fn(filename)

            if field.url_relative_path:
                filename = urljoin(field.url_relative_path, filename)

            yield get_url(field.endpoint, filename=filename), 

class MultipleImageUploadField(ImageUploadField):
    """
        Multiple image upload field.
        Does image validation, thumbnail generation, updating and deleting images.
        Requires PIL (or Pillow) to be installed.
    """

    widget = MultipleImageUploadInput()

    def process(self, formdata, data=unset_value):
        self.formdata = formdata

        return super(MultipleImageUploadField, self).process(formdata, data)

    def process_formdata(self, valuelist):
        self.data = list()

        for value in valuelist:
            if self._is_uploaded_file(value):
                self.data.append(value)

    def populate_obj(self, obj, name):
        field = getattr(obj, name, None)

        if field:
            filenames = ast.literal_eval(field)

            for filename in filenames[:]:

                if "_{}-delete".format(filename) in self.formdata.keys():
                    self._delete_file(filename)
                    filenames.remove(filename)

        else:

            filenames = list()

        for data in self.data:

            if self._is_uploaded_file(data):

                try:
                    self.image = Image.open(data)
                except Exception as e:
                    raise ValidationError('Invalid image: %s' % e)

                filename = self.generate_name(obj, data)
                filename = self._save_file(data, filename)
                data.filename = filename

                filenames.append(filename)

        setattr(obj, name, str(filenames))
