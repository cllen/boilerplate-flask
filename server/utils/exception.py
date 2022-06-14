from functools import wraps
from flask import request,current_app
from marshmallow import ValidationError
from exceptions import  JSONException,HTMLException
from flask import render_template

from utils.login import current_user

def catch_exception(func):

    @wraps(func)
    def wrapper2(*args,**kwargs):

        try:
            return func(*args,**kwargs)
        except HTMLException as e:
            return render_template(
                'home/error.html',
                http_code=e.code,
                error_code=e.error_code,
                error_message=e.error_message,
                current_app=current_app,
                current_user=current_user
            )
        except Exception as e:
            raise e

    return wrapper2

            

