import abc
from ..._wxapi.get_phone_number import get_phone_number
from ...exceptions import (
	RequestFrequency,
	CodeInvalid,
	UnexpectedError,
)


class PhoneNumberMixin:

	@property
	@abc.abstractmethod
	def access_token(self):
		pass 

	def get_phone_number(user,code):
		json_response = get_phone_number(self.access_token,code)
		
		if json_response['errcode'] == 0:
			self._update_user(user,{'mobile':json_response['phone_info']})
		elif json_response['errcode'] == -1:
			raise RequestFrequency('request frequency!')
		elif json_response['errcode'] == 40029:
			raise CodeInvalid('invalid code!')
		else:
			raise UnexpectedError('unexpected error!')
		return json_response['phoneNumber']