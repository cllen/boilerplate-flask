from ._imports_ import *

# 第三方
logger = logging.getLogger(__name__)

# 自己的库

# 业务代码

@bp_base.route('/',methods=('GET',))
def indexbase():
	return redirect(url_for('mp-view.index'))

@bp.route('/',methods=('GET',))
@bp.route('/index',methods=('GET',))
@bp.route('/index/',methods=('GET',))
def index():
	return render_template(
		'mp/index.html', 
		current_app=current_app,
		current_user=current_user,	
	)