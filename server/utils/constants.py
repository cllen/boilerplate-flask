class UserRole:
	USER = '普通用户'
	ADMIN = '管理员'

class UserType:
	BASE = 'base'
	BASIC_HTTP = 'basic http'
	WECHAT = '微信'
	ALIPAY = '支付宝'

class UserPermission:
	USER = 0x01 * 2 ** 0
	ADMIN = 0x01 * 2 ** 1

class UserStatus:
	ACTIVE = '活动'
	INACTIVE = '冻结'

class FilePermission:
	PUBLIC = '公开'
	PRIVATE = '不公开'

class AdminAccessErrorReason:
	NOT_ADMIN = '不是管理员'
	NOT_LOGINED = '未登录'
