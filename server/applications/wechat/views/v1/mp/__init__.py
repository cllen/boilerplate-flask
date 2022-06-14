from flask import Blueprint
from flask_restx import Api

bp = Blueprint('mp-view',__name__)

bp_base = Blueprint('mp-view-base',__name__)

from . import (
	index,
)