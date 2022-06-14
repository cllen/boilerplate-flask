from functools import wraps
from flask import request
from marshmallow import ValidationError
from exceptions import  JSONException,HTMLException

from json2html import json2html

import json

import logging
logger = logging.getLogger(__name__)

def parse_with(Schema,ExceptionType,location='args'):

    def wrapper1(func):

        @wraps(func)
        def wrapper2(*args,**kwargs):

            schema = Schema()
            try:
                result = schema.load(getattr(request,location))
                # logger.debug('>>>parse_with ')
                # logger.debug(result)
            except ValidationError as e:
                raise ExceptionType(10003,error_message=json2html.convert(json=e.messages))
            except Exception as e:
                logger.debug(e)
                raise ExceptionType(10001,error_message=e)
            request.parsed = result
            return func(*args,**kwargs)
        return wrapper2
    return wrapper1

            

