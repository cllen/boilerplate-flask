from ._imports_ import *

from utils.login import (
    parse_username_password,
    make_login_required_response,
    set_user,
    
)
from ..services import login

@bp.route('/home',methods=('GET',))
def home():
    return render_template(
        'admin/home.html',
        current_app=current_app,
        current_user=current_user,
    )
