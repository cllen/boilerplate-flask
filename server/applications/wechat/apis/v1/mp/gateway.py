#coding:utf8
from ._imports_ import *
logger = logging.getLogger(__name__)

from ....schemas.parsers.mpapp.gateway import(
	Verification as VerificationParser,
)
"""
	用户接受微信通知的接口
"""
@ns.route('/gateway')
class Gateway(Resource):

	@ns.doc(parser=VerificationParser)
	@parse_with(parser=VerificationParser,exception=JSONException)
	def get(self):

		payload = VerificationParser.parse_args()

		try:
			check_signature(payload['signature'], payload['timestamp'], payload['nonce'])
		except:
			logger.error(
				'Checking signature failed. payload %s Err: %s',
				payload,
				traceback.format_exc(),
			)
			return ''
		return payload['echostr']


	@ns.doc(parser=VerificationParser)
	def post(self):

		try:
			mpauth = MpAuth()
			payload = mpauth.parse_message(request.data.decode('utf8'))
			logger.info('>>> received payload type: %s', type(payload))

			# 关注事件
			if isinstance(payload, EVENT_TYPES['subscribe']):
				logger.info('>>> sub source: %s', payload.source)
				logger.info(dict(payload._data))
				msg = '''
					<xml>
						<ToUserName><![CDATA[%s]]></ToUserName>
						<FromUserName><![CDATA[%s]]></FromUserName>
						<CreateTime>%s</CreateTime>
						<MsgType><![CDATA[text]]></MsgType>
						<Content><![CDATA[%s]]></Content>
					</xml>'''%(
						dict(payload._data)['FromUserName'],
						dict(payload._data)['ToUserName'],
						str(int(time.time())),
						"thanks for your subscribing",)

				logger.info(msg)

				return msg

			# 取消关注时间
			elif isinstance(payload, EVENT_TYPES['unsubscribe']):
				logger.info('>>>>unsub source: %s', payload.source)

		except:
			pass
		return ''
