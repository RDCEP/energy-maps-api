from flask import Blueprint
from energy_maps_api.constants import URL_PREFIX


bp = Blueprint('update', __name__,
               url_prefix=URL_PREFIX)


@bp.route('/update', methods=['PUT', 'PATCH'])
def update():
    return 'Update resource'
