#coding:utf8
from ._imports_ import *
logger = logging.getLogger(__name__)

from ....schemas.parsers.miniapp.user import(
	Post as PostParser,
	Put as PutParser,
)

from ....schemas.marshals.miniapp.user import(
	Post as PostMarshal,
	Put as PutMarshal,
)

@ns.route('/user')
class Single(Resource):

	@ns.doc(parser=PostParser)
	# @catch_exception()
	@parse_with(parser=PostParser,exception=JSONException)
	@ns.marshal_with(PostMarshal)
	def post(self):

		args = PostParser.parse_args()

		miniappauth = MiniappAuth()
		token,user = miniappauth.login_by_code(args['code'])

		return {
			'error_code':0,
			'token':token,
		}

	@ns.doc(parser=PutParser)
	# @catch_exception()
	@auth(exception=JSONException)
	@parse_with(parser=PutParser,exception=JSONException)
	@ns.marshal_with(PutMarshal)
	def put(self):

		args = PutParser.parse_args()

		miniappauth = MiniappAuth()
		user = miniappauth.update_profile(
			user=request.user,
			iv=args['iv'],
			encrypted_data=args['encrypted_data']
		)

		return {
			'error_code':0,
			'user':user,
		}

