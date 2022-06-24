#coding:utf8
from ._imports_ import *
logger = logging.getLogger(__name__)

from ....schemas.parsers.mpapp.callback import(
	Get as GetParser,
)

"""
	相当于孟哥的oauth接口
"""
@ns.route('/callback')
class Callback(Resource):

	@ns.doc(parser=GetParser)
	@parse_with(parser=GetParser,exception=JSONException)
	def get(self):

		# args = request.get_json()
		# code = args.get('code')
		# state = args.get('state')
		payload = GetParser.parse_args()
		
		mpauth = MpAuth()

		# 第三方开发者拿着code请求微信服务器，换用户信息。
		token,user = mpauth.oauth_login(code=payload['code'])

		# 记录登录状态
		session['user'] = {'id':user.id}

		# 用标识（授权前给的）换取授权前地址，并且跳过去。
		redirect_url = mpauth.retrieve_beforeauthorize_url(state=payload['state'])

		return redirect(redirect_url)
