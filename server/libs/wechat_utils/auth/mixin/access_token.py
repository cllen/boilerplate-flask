import abc
from ..._wxapi.access_token import get_access_token_from_wx
from ...exceptions import (
	RequestFrequency,
	WrongAppSecret,
	UnexpectedError,
)


class AccessTokenMixin:

	@property
	@abc.abstractmethod
	def _get_access_token(self):
		pass

	@property
	@abc.abstractmethod
	def _save_access_token(self,access_token):
		pass
	
	@property
	def access_token(self):

		access_token = self._get_access_token()

		if not access_token:
			json_response = get_access_token_from_wx(
				appid=self.appid,
				app_secret=self.app_secret
			)

			if json_response['errcode'] == 0:
				self._save_access_token(json_response['access_token'])
				return json_response['access_token']
			elif json_response['errcode'] == -1:
				raise RequestFrequency('request frequency!')
			elif json_response['errcode'] == 40001:
				raise WrongAppSecret('wrong app_secret!')
			else:
				raise UnexpectedError('unexpected error!')
		else:
			return access_token

		
