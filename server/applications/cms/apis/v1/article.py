#coding:utf8
from ._imports_ import *
logger = logging.getLogger(__name__)

from ...schemas.parsers.article import(
	article as articleParser,
)

@ns.route('/article')
class Article(Resource):

	@ns.doc(parser=articleParser)
	def get(self):

		args = articleParser.parse_args()

		# This is FileStorage instance
		file = args['iamge']  
		video = args['video']

		