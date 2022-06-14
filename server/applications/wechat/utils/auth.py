from functools import wraps
import traceback

import logging
logger = logging.getLogger(__name__)

from flask import (
	request,
	session,
)

from libs.wechat_utils.auth import (
	BaseMiniappAuth,
	BaseMpAuth,

	PhoneNumberMixin,
	AccessTokenMixin,
)

from libs.wechat_utils.constants import Keys

from libs.meta import Singleton

from applications import db

from ..models import (
	WechatUser as WechatUserModel,
)

from .settings import WechatSettings
from .redis import WechatRedis

from exceptions import JSONException

tmp_store = {}

wechat_settings = WechatSettings()
wechat_redis = WechatRedis()

class MiniappAuth(
	BaseMiniappAuth,

	PhoneNumberMixin, 
	AccessTokenMixin,
	metaclass=Singleton):

	TOKEN_EXPIRED = JSONException(12101)
	TOKEN_CORRUPTED = JSONException(12102)
	TOKEN_DECRYPT_FAIL = JSONException(12103)
	MISSING_TOKEN = JSONException(12104)
	OPENID_NOT_FOUND = JSONException(12105)
	CODE_INVALID = JSONException(12106)
	REQUEST_FREQUENCY = JSONException(12107)
	USERINFO_DECRYPT_FAILED = JSONException(12108)
	UNEXPECTED_ERROR = JSONException(12109)

	@property
	def appid(self):
		return wechat_settings.appid

	@property
	def app_secret(self):
		return wechat_settings.app_secret

	@property
	def token_secret_key(self):
		return wechat_settings.token_secret_key

	@property
	def token_salt(self):
		return wechat_settings.token_salt

	@property
	def token_expiration(self):
		return wechat_settings.token_expiration

	def _get_user_by_openid(self,openid):
		try:
			return WechatUserModel.query.filter_by(openid=openid).first()
		except:
			return None

	def _save_user(self,userinfo):
		wechat_user = WechatUserModel(**userinfo)
		db.session.add(wechat_user)
		db.session.commit()

	def _update_user(self,openid,decrypted_data):
		wechat_user = self._get_user_by_openid(openid)
		for key,value in decrypted_data.items():
			setattr(wechat_user,key,value)
		db.session.commit()
		wechat_user = self._get_user_by_openid(openid)
		return wechat_user

	@property
	def _get_access_token(self):
		if wechat_redis.base_redis.client:
			return wechat_redis.base_redis.get(Keys.access_token)
		else:
			return tmp_store.get(Keys.access_token)

	@property
	def _save_access_token(self,access_token):
		if wechat_redis.base_redis.client:
			wechat_redis.base_redis.set(Keys.access_token,access_token)
		else:
			tmp_store[Keys.access_token] = access_token


class MpAuth(BaseMpAuth, metaclass=Singleton):

	@property
	def appid(self):
		return wechat_settings.appid

	@property
	def app_secret(self):
		return wechat_settings.app_secret

	@property
	def token_secret_key(self):
		return wechat_settings.token_secret_key

	@property
	def token_salt(self):
		return wechat_settings.token_salt

	@property
	def token_expiration(self):
		return wechat_settings.token_expiration

	@property
	def callback_url(self):
		return wechat_settings.oauth_callback_url

	@property
	def post_beforeauthorize_default(self):
		return wechat_settings.post_oauth_beforeauthorize_url_default

	def _persist_beforeauthorize_url(self,token, referrer):
		if wechat_redis.base_redis.client is not None:
			wechat_redis.persist_beforeauthorize(token,referrer)
		else:
			tmp_store[token]=referrer

	def _retrieve_beforeauthorize_url(self, state):
		if wechat_redis.base_redis.client is not None:
			return wechat_redis.retrieve_beforeauthorize(state)
		else:
			return tmp_store.get(state)

	def _get_user_by_openid(self, openid):
		try:
			return WechatUserModel.query.filter_by(openid=openid).first()
		except Exception as e:
			return None

	def _save_user(self, **kargs):
		try:
			wechat_user = WechatUserModel(**kargs)
			db.session.add(wechat_user)
			db.session.commit()
			return wechat_user
		except Exception as e:
			raise JSONException(error_code=10004)


	def _update_user(self,openid,decrypted_data):
		wechat_user = self._get_user_by_openid(openid)
		for key,value in decrypted_data.items():
			setattr(wechat_user,key,value)
		db.session.commit()
		wechat_user = self._get_user_by_openid(openid)
		return wechat_user


def auth(exception=JSONException):

	def wrapper1(func):

		@wraps(func)
		def wrapper2(*args,**kwargs):

			token = request.environ.get('HTTP_TOKEN')
			miniappauth = MiniappAuth()
			logger.debug(token)
			if not token:
				raise exception(error_code=12104)

			user = miniappauth.login_by_token(token)
			request.user = user

			return func(*args,**kwargs)
		return wrapper2
	return wrapper1

from flask import has_request_context, _request_ctx_stack
from werkzeug.local import LocalProxy

current_user = LocalProxy(lambda: _get_user())

def _get_user():
	user_key = 'user'
	if has_request_context() and hasattr(_request_ctx_stack.top, user_key) and _request_ctx_stack.top.user != None:
		return getattr(_request_ctx_stack.top, user_key)

	elif session.get(user_key) is not None:
		try:
			user = WechatUserModel.query.filter_by(id=session.get(user_key)['id'])[0]
			setattr(_request_ctx_stack.top, user_key, user)
			return user
		except Exception as e:
			return None
	elif request and request.environ.get('HTTP_TOKEN'):
			token = request.environ.get('HTTP_TOKEN')
			miniappauth = MiniappAuth()
			user = miniappauth.login_by_token(token)
			return user
	else:
		return None
