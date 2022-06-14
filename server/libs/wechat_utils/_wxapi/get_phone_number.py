#coding:utf8
import requests

import logging
logger = logging.getLogger(__name__)

def get_phone_number(access_token,code):

	response = requests.post(
		'https://api.weixin.qq.com/wxa/business/getuserphonenumber',
		data={
			'access_token':access_token,
			'code':code,
		}
	)
	return response.json()

