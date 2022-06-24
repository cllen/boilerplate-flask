#coding:utf8
from ._imports_ import *
logger = logging.getLogger(__name__)

# from ....schemas.parser.mp.authorize import (
# 	Get as GetParser,
# )

"""
	相当于孟哥的locator接口
"""
@ns.route('/authorize')
class Authorize(Resource):
	@ns.doc()
	# @parse_with(parser=GetParser,exception=JSONException)
	def get(self):
		mpauth = MpAuth()
		redirect_url = mpauth.generate_authorize_url(request.referrer)
		return redirect(redirect_url)
