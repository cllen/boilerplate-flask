#coding:utf8

import redis
import traceback
from abc import ABCMeta, abstractmethod
import logging
logger = logging.getLogger(__name__)

class BaseWechatRedis:

	@property
	@abstractmethod
	def base_redis(self):
		return None
