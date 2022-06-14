from flask import Blueprint
from flask_restx import Api

bp = Blueprint('mp-api',__name__)
api = Api(bp)

from . import (
	authorize,
	callback,
	gateway,
)