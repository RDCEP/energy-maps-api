from flask import Blueprint
from energy_maps_api.constants import URL_PREFIX
from flask import render_template
from flask import request
# not sure which logging package to use
# from flask import log
# import logging
# from energy_maps_api import app
from energy_maps_api.app import app

bp = Blueprint('errors', __name__, url_prefix=URL_PREFIX)


def error_response(status):
    return app.logger.error('Error: %s\n %s\n%s\n%s', status, request.headers, request.get_data, request.url)


@bp.errorhandler(400)
def bad_request():
    error_response('400 Bad Request')
    return render_template('errors/400.html'), 400


@bp.errorhandler(404)
def not_found(error):
    error_response('404 Not Found')
    return render_template('errors/404.html'), 404


@bp.errorhandler(403)
def forbidden_access(error):
    error_response('403 Forbidden')
    return render_template('errors/403.html'), 403


@bp.errorhandler(409)
def conflict(error):
    error_response('409 Conflict')
    return render_template(('errors/409.html')), 409


@bp.errorhandler(500)
def internal_server(error):
    error_response('500 Internal Server Error')
    return render_template('errors/500.html'), 500
