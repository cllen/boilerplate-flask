import logging
logger = logging.getLogger(__name__)

import traceback
import abc
from abc import ABC
from itsdangerous import SignatureExpired, BadTimeSignature, BadSignature

from ..decrypt import Decrypt
from .._wxapi.userinfo import get_session_key_from_wx,decrypt_wechat_user

from ..exceptions import (
	TokenExpired,
	TokenCorrupted,
	TokenDecryptFailed,
	MissingToken,
	OpenidNotFound,
	CodeInvalid,
	RequestFrequency,
	UserinfoDecryptFailed,
	UnexpectedError,
)

"""
suage
=====

from libs.wechat_utils.auth import (
	BaseMiniappAuth,
	PhoneNumberMixin,
	AccessTokenMixin,
)
from werkzeug.exceptions import HTTPException

class MiniappAuth(
	BaseMiniappAuth,

	PhoneNumberMixin, 
	AccessTokenMixin,
	metaclass=Singleton):
 
	# flask
	TOKEN_EXPIRED = HTTPException(12101)

	@property
	def appid(self):
		return 'xxx'

	@property
	def app_secret(self):
		return 'xxx'

	@property
	def token_secret_key(self):
		return 'xxx'

	@property
	def token_salt(self):
		return 'xxx'

	@property
	def token_expiration(self):
		return 99999

	@property
	def _get_access_token(self):
		return 'xxx'

	@property
	def _save_access_token(self,access_token):
		return None

	def _save_user(self,userinfo):
		return None

	def _update_user(self,openid,decrypted_data):
		return None

miniappauth = MiniappAuth()
token,user = miniappauth.login_by_code(code='xxx')
"""

class BaseMiniappAuth:

	TOKEN_EXPIRED = TokenExpired('Token expired!')
	TOKEN_CORRUPTED = TokenCorrupted('Token corrupted!')
	TOKEN_DECRYPT_FAIL = TokenDecryptFailed('Token decrypted fail!')
	MISSING_TOKEN = MissingToken('Missing token!')
	OPENID_NOT_FOUND = OpenidNotFound('Openid not found!')
	CODE_INVALID = CodeInvalid('Code invalid!')
	REQUEST_FREQUENCY = RequestFrequency('request frequency!')
	USERINFO_DECRYPT_FAILED = UserinfoDecryptFailed('userinfo decrypt failed!')
	UNEXPECTED_ERROR = UnexpectedError('unexpected error!')
	APPID_INVALID = CodeInvalid('appid invalid!')

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



	@abc.abstractmethod
	def _get_user_by_openid(self,openid):
		pass

	@abc.abstractmethod
	def _save_user(self,userinfo):
		pass

	@abc.abstractmethod
	def _update_user(self,openid,decrypted_data):
		pass

	def login_by_code(self,code):
		_userinfo,url = get_session_key_from_wx(
			appid=self.appid,
			appsecret=self.app_secret,
			js_code=code
		)
		logger.error('>> login_by_code')
		logger.error(_userinfo)
		logger.error(url)
		if _userinfo.get('errcode') == 40029:
			raise self.CODE_INVALID
		elif _userinfo.get('errcode') == 45011:
			raise self.REQUEST_FREQUENCY
		elif _userinfo.get('errcode') == 40013:
			raise self.APPID_INVALID
		elif _userinfo.get('errcode') in [0, None, ]:
			pass
		else:
			self.UNEXPECTED_ERROR.error_message = "未知错误！微信服务器错误代码：".format(_userinfo.get('errcode'))
			raise self.UNEXPECTED_ERROR

		try:
			userinfo = {
				'openid':_userinfo['openid'],
				'session_key':_userinfo['session_key'],
				'unionid':_userinfo.get('unionid'),
			}
		except Exception as e:
			logger.error(_userinfo)
			logger.error(url)
			raise e


		user = self._get_user_by_openid(openid=userinfo.get('openid'))
		logger.error(user)
		if not user:
			logger.error(user)
			self._save_user(userinfo=userinfo)
			user = self._get_user_by_openid(openid=userinfo.get('openid'))
		else:
			self._update_user(openid=userinfo.get('openid'),decrypted_data=userinfo)

		token = Decrypt.encrypt(
			data={'openid':str(user.openid)},
			secret_key=self.token_secret_key,
			salt=self.token_salt,
			expires_in=int(self.token_expiration)
		)
		return str(token),user

	def login_by_token(self,token):
		try:
			data = Decrypt.decrypt(
				token=token,
				secret_key=self.token_secret_key,
				salt=self.token_salt,
				expires_in=int(self.token_expiration)
			)
		except SignatureExpired:
			logger.error('Token expired for: %s', token)
			raise self.TOKEN_EXPIRED
		except (BadSignature, BadTimeSignature):
			logger.error('Token corrupted: %s', token)
			raise self.TOKEN_CORRUPTED
		except Exception as e:
			logger.error('Unexpected decrypt error: %s', token)
			raise self.TOKEN_DECRYPT_FAIL

		if not data.get('openid'):
			logger.error('Token missing openid: %s', token)
			raise self.MISSING_TOKEN

		user = self._get_user_by_openid(openid=data.get('openid'))

		if user is None:
			logger.error('User is not found with openid: %s', data.get('openid'))
			raise self.OPENID_NOT_FOUND
		return user

	def update_profile(self,user,iv,encrypted_data):
		try:
			decrypted_data = decrypt_wechat_user(
				session_key=user.session_key, 
				iv=iv,
				encrypted_data=encrypted_data
			)
		except Exception as e:
			logger.error(traceback.format_exc())
			raise self.USERINFO_DECRYPT_FAILED

		userinfo = {}

		if decrypted_data.get('openId'):
			userinfo.update({'openid':str(decrypted_data.get('openId'))})
		if decrypted_data.get('nickName'):
			userinfo.update({'nickname':str(decrypted_data.get('nickName'))})
		if decrypted_data.get('gender'):
			userinfo.update({'gender':str(decrypted_data.get('gender'))})
		if decrypted_data.get('language'):
			userinfo.update({'language':str(decrypted_data.get('language'))})
		if decrypted_data.get('city'):
			userinfo.update({'city':str(decrypted_data.get('city'))})
		if decrypted_data.get('province'):
			userinfo.update({'province':str(decrypted_data.get('province'))})
		if decrypted_data.get('country'):
			userinfo.update({'country':str(decrypted_data.get('country'))})
		if decrypted_data.get('avatarUrl'):
			userinfo.update({'avatar':str(decrypted_data.get('avatarUrl'))})
		if decrypted_data.get('phoneNumber'):
			userinfo.update({'mobile':str(decrypted_data.get('phoneNumber'))})
		if decrypted_data.get('purePhoneNumber'):
			userinfo.update({'purePhoneNumber':str(decrypted_data.get('purePhoneNumber'))})
		if decrypted_data.get('countryCode'):
			userinfo.update({'countryCode':str(decrypted_data.get('countryCode'))})

		logger.info(userinfo)
		user = self._update_user(user.openid,userinfo)
		return user