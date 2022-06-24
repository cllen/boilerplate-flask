#coding:utf8
import json
import time
from ..constants import RedisKeys

class ThrottleMixin:

	throttle_expired = 60*60*24

	def throttle_get(self,openid,seconds=60):
		return self._throttle_get(
			RedisKeys.throttle.format(openid),
			seconds
		)

	def throttle_set(self,openid):
		return self._throttle_set(
			RedisKeys.throttle.format(openid)
		)

	def _throttle_get(self,key,seconds):

		value = self.get(key)
		current_time = time.time()

		if value:
			try:
				historys = json.loads(value)
				
				# 最后一个时间是最远时间，删除
				while historys and historys[-1] < current_time - seconds:
					historys.pop()

				_historys = json.dumps(historys)

				self.set(key,expires_in=self.throttle_expired,value=_historys)

				return historys
			except:
				return []
		else:
			return []

	def _throttle_set(self,key):
		value = self.get(key)
		current_time = time.time()
		if value:
			try:
				historys = json.loads(value)
			except:
				historys = []
			
				# 第一个时间是现在时间，插入
				historys.insert(0,current_time)

				_historys = json.dumps(historys)

				self.set(key,expires_in=self.throttle_expired,value=_historys)

				return True
		else:
			return False