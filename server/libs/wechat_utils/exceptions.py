class TokenExpired(Exception):
	pass
class TokenCorrupted(Exception):
	pass
class TokenDecryptFailed(Exception):
	pass
class MissingToken(Exception):
	pass
class OpenidNotFound(Exception):
	pass
class CodeInvalid(Exception):
	pass
class RequestFrequency(Exception):
	pass
class UserinfoDecryptFailed(Exception):
	pass
class UnexpectedError(Exception):
	pass


# 获取access_token
class WrongAppSecret(Exception):
	pass