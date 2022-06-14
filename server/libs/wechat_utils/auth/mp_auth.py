#coding:utf8
import hashlib
import logging
logger = logging.getLogger(__name__)
from six.moves.urllib.parse import quote

import abc

# 第三方
from wechatpy import WeChatOAuth
from wechatpy import parse_message
from wechatpy.utils import check_signature, random_string


from ..decrypt import Decrypt
from ..common import Random

class BaseAuth:

	"""
		1. 提供重定向功能
		1. 需要实现获取用户方法
	"""

	access_token_url = 'https://api.weixin.qq.com/cgi-bin/token'
	oauth_scope = 'snsapi_userinfo'
	oauth_base_url = 'https://open.weixin.qq.com/connect/'

	@property
	@abc.abstractmethod
	def appid(self):
		pass

	@property
	@abc.abstractmethod
	def app_secret(self):
		pass

	@property
	@abc.abstractmethod
	def token_secret_key(self):
		pass

	@property
	@abc.abstractmethod
	def token_salt(self):
		pass

	@property
	@abc.abstractmethod
	def token_expiration(self):
		pass

	@property
	@abc.abstractmethod
	def callback_url(self):
		pass

	@property
	@abc.abstractmethod
	def post_beforeauthorize_default(self):
		pass

	@abc.abstractmethod
	def _persist_beforeauthorize_url(self,token, referrer):
		"""
			将用户的授权前地址保存起来。
			@param <token>: 用户token
			@param <referrer>: 用户登录前的url
		"""
		pass

	@abc.abstractmethod
	def _retrieve_beforeauthorize_url(self, state):
		"""
			将用户的授权前地址检索出来。
			@param <token>: 用户token
			@param <referrer>: 用户登录前的url
		"""
		pass

	@abc.abstractmethod
	def _get_user_by_openid(self, openid):
		pass

	@abc.abstractmethod
	def _save_user(self, openid):
		pass

	@abc.abstractmethod
	def _update_user(self,openid,decrypted_data):
		pass

	@property
	def oauth(self):
		return WeChatOAuth(
			self.appid,
			self.app_secret,
			self.callback_url,
			self.oauth_scope,
		)

	def _generate_authorize_url(self, state=None):
		callback_url = quote(self.callback_url, safe=b'')
		url_list = [
			self.oauth_base_url,
			'oauth2/authorize?appid=',
			self.appid,
			'&redirect_uri=',
			callback_url,
			'&response_type=code&scope=',
			self.oauth_scope
		]
		if state:
			url_list.extend(['&state=', state])
		url_list.append('#wechat_redirect')
		logger.info('>>> {}'.format(url_list))
		return ''.join(url_list)

	def generate_authorize_url(self, referrer):

		logger.debug('>> generate_authorize_url')
		logger.debug(referrer)

		"""
			#1 这个流程首先从这个接口开始
				1. 保存用户【授权前地址】并得到该标识
				2. 让前端重定向到微信授权api，带上callback回调接口、标识。
				3. 下一步微信授权接口会将标识、code交给前端、让前端重定向到callback
		"""

		if not referrer:
			referrer = self.post_beforeauthorize_default
		logger.debug(referrer)
		md5 = hashlib.md5(referrer.encode('utf8')).hexdigest()
		token = Random.generate(8, suffix=md5)
		self._persist_beforeauthorize_url(token, referrer)
		return self._generate_authorize_url(token)

	def oauth_login(self,code):

		"""
			#2 在callback接口调用此方法
				1. 请求微信获取用户信息api，带上code。（使用第三方库实现该功能）
		"""

		res = self.oauth.fetch_access_token(code)
		user = self._get_user_by_openid(openid=res.get('openid'))

		if user is None:
			user = self._save_user(openid=res['openid'])

		user_info_raw = self.oauth.get_user_info(res['openid'], res['access_token'])
		user_info = {
			'openid': user_info_raw['openid'],
			'nickname': user_info_raw.get('nickname'),
			'unionid': user_info_raw.get('unionid'),
			'avatar': user_info_raw.get('headimgurl'),
			'gender': user_info_raw.get('sex'),
			'city': user_info_raw.get('city'),
			'province': user_info_raw.get('province'),
			'country': user_info_raw.get('country'),
			'language': user_info_raw.get('language'),
		}
		self._update_user(user.openid,user_info)

		token = Decrypt.encrypt(
			data={'openid':str(user.openid)},
			secret_key=self.token_secret_key,
			salt=self.token_salt,
			expires_in=self.token_expiration
		)

		user = self._get_user_by_openid(openid=res.get('openid'))
		
		return token,user


	def retrieve_beforeauthorize_url(self,state):
		"""
			#3 还是在callback调用此接口
				1. 用标识检索用户授权前地址，并且让前端重定向。
		"""
		if state:
			redirect_url = self._retrieve_beforeauthorize_url(state)
			if redirect_url:
				return redirect_url
		return self.post_beforeauthorize_default

	def parse_message(self, xml_payload):
		"""
			解析微信发过来的消息，如订阅等。
		"""
		return parse_message(xml_payload)
