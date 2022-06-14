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

@api.route('/user')
class Single(Resource):

	@api.doc(parser=PostParser)
	@catch_exception()
	@parse_with(parser=PostParser,exception=JSONException)
	@api.marshal_with(PostMarshal)
	def post(self):

		args = PostParser.parse_args()

		miniappauth = MiniappAuth()
		token,user = miniappauth.login_by_code(args['code'])

		return {
			'error_code':0,
			'token':token,
		}

	@api.doc(parser=PutParser)
	@catch_exception()
	@auth(exception=JSONException)
	@parse_with(parser=PutParser,exception=JSONException)
	@api.marshal_with(PutMarshal)
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

