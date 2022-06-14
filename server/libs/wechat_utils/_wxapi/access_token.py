#coding:utf8
import requests

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_access_token_from_wx(appid,app_secret):

	url_list = [
		'https://api.weixin.qq.com/cgi-bin/token?',
		'grant_type=client_credential&',
		'appid=',
		appid,
		'&secret=',
		app_secret,
	]

	url = "".join(url_list)
	response = requests.get(url)
	return response.json()

