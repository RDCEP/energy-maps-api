from flask import Blueprint

bp = Blueprint('delete', __name__, static_folder='static', template_folder='templates')

@bp.route('/delete')
def delete_infrastructure():
    return 'delete operation'