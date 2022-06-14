from flask import Blueprint

bp = Blueprint('base-views',__name__)

from . import (
    home,
    login,
)