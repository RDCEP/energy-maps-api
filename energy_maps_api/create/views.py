from flask import Blueprint

bp = Blueprint('create', __name__, static_folder='static', template_folder='templates')

@bp.route('/upload', methods=['POST'])
def upload():
    return 'Upload infrastructure type'