from flask import Blueprint
from energy_maps_api.constants import URL_PREFIX
from flask import render_template
from flask import request
# not sure which logging package to use
from flask import log
import logging

bp = Blueprint('retrieve', __name__, url_prefix=URL_PREFIX)

def error_response(status):
    return app.logger.error('Error: %s\n %s\n%s\n%s', status, request.headers, request.get_data, request.url)

@bp.errorhandler(404)
def not_found(error):
    error_response('404 Not Found')
    return render_template('errors/404.html'), 404


@bp.errorhandler(403)
def forbidden_access(error):
    error_response('403 Forbidden')
    return render_template('errors/403.html'), 403


@bp.errorhandler(500)
def internal_server(error):
    error_response('500 Internal Server Error')
    return render_template('errors/500.html'), 500
