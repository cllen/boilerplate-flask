from .base import AppException
from .error_messages import error_messages

class HTMLException(AppException):
	co_msg_mapping = error_messages

class JSONException(AppException):
	co_msg_mapping = error_messages
