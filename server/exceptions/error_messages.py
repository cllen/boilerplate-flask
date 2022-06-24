"""
	10000 系统错误
	11000 base模块错误
	12000 wechat模块错误
	13000 cms模块错误
"""

error_messages = {
	
	# 公用部分
	10001:{
		'error_message':"未知错误！",
		'http_code':500,
	},
	10002:{
		'error_message':"用户未登录！",
		'http_code':400,
	},
	10003:{
		'error_message':"参数错误!",
		'http_code':400,
	},
	10004:{
		'error_message':"数据库读写错误!",
		'http_code':400,
	},

	10005:{
		'error_message':"_get_user时候错误！",
		'http_code':405,
	},

	# 微信模块部分（小程序、公众号）
	12101:{
		'error_message':"token过期！",
		'http_code':405,
	},
	12102:{
		'error_message':"token毁坏！",
		'http_code':400,
	},
	12103:{
		'error_message':"token解密失败！",
		'http_code':400,
	},
	12104:{
		'error_message':"请求时候缺少token！",
		'http_code':400,
	},
	12105:{
		'error_message':"用户openid在数据库无法找到！",
		'http_code':400,
	},
	12106:{
		'error_message':"code非法！请检查管理后台是否设置正确的appid！",
		'http_code':400,
	},
	12107:{
		'error_message':"请求微信服务器过于频繁！",
		'http_code':400,
	},
	12108:{
		'error_message':"userinfo解密失败！",
		'http_code':400,
	},
	12109:{
		'error_message':"未知错误！",
		'http_code':400,
	},
	12110:{
		'error_message':"管理后台设置的appid非法！",
		'http_code':400,
	},

	# cms模块部分
	# 略

}