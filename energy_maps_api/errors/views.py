from flask import Blueprint
from energy_maps_api.constants import URL_PREFIX
from flask import render_template

bp = Blueprint('retrieve', __name__, url_prefix=URL_PREFIX)

# consider spitting back the request someone made
@bp.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404


@bp.errorhandler(403)
def forbidden_access(error):
    return render_template('errors/403.html'), 403


@bp.errorhandler(500)
def internal_server(error):
    return render_template('errors/500.html'), 500
