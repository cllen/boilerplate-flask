import logging
import traceback
from flask_restx import Resource

from flask import (
	current_app,
	redirect,
	request,
	session,
)

from . import api

# from ....utils.parser import parse_with

from exceptions import JSONException

ns = api.namespace('cms')