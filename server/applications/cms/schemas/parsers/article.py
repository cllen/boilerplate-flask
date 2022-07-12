from werkzeug.datastructures import FileStorage
from ...apis.v1 import api
article = api.parser()
article.add_argument('iamge', location='files',
    type=FileStorage, required=False)
article.add_argument('video', location='files',
    type=FileStorage, required=False)
