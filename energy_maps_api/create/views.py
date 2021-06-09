from flask import Blueprint
from energy_maps_api.constants import URL_PREFIX

bp = Blueprint('create', __name__, static_folder='static', template_folder='templates', url_prefix=URL_PREFIX)

@bp.route('/upload', methods=['POST'])
def upload():
    return 'Upload infrastructure type'