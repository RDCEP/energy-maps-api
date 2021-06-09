from flask import Blueprint

bp = Blueprint('update', __name__, static_folder='static', template_folder='templates')

@bp.route('/update', methods=['PUT', 'PATCH'])
def update():
    return 'Update resource'