from flask import session
import abc
from libs.meta import Singleton

class BaseTempStorage(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def set(self,key,value):
        pass

    @abc.abstractmethod
    def get(self,key):
        pass

class SessionTempStorage(BaseTempStorage):

    def set(self,key,value):
        session[key] = value
        return True

    def get(self,key):
        return session.get(key)

temp_storage = SessionTempStorage()