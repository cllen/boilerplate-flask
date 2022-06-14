#coding:utf8

# crypt
import base64
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7

import requests
import json
import time
import traceback
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_session_key_from_wx(appid,appsecret,js_code):
	weixin_api = 'https://api.weixin.qq.com/sns/jscode2session'
	grant_type = 'authorization_code'
	url = '{}?appid={}&secret={}&js_code={}&grant_type={}'.format(
		weixin_api,
		appid,
		appsecret,
		js_code,
		grant_type,
	)
	return requests.get(url).json(),url

def decrypt_wechat_user(session_key, iv, encrypted_data):

	# 对称解密的目标密文
	encrypted_data = base64.b64decode(encrypted_data)

	# 对称解密秘钥 aeskey
	key = base64.b64decode(session_key)

	# 对称解密算法初始向量
	iv = base64.b64decode(iv)

	# cipher包含三种保护机密数据的加密算法：对称加密算法、非对称加密算法、混合型加密算法
	cipher = Cipher(
		algorithms.AES(key),
		modes.CBC(iv),
		backend=default_backend(),
	)
	decryptor = cipher.decryptor()
	plain = decryptor.update(encrypted_data) + decryptor.finalize()
	unpadder = PKCS7(128).unpadder()
	decrypted = unpadder.update(plain)
	decrypted += unpadder.finalize()
	decrypted = json.loads(decrypted.decode('utf8'))
	return decrypted