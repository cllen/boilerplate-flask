from flask import Blueprint
from flask_restx import Api

bp = Blueprint('wechat-view',__name__)

from .mp import (
	index,
)