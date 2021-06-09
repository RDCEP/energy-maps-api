from flask import Blueprint

bp = Blueprint('retrieve', __name__, static_folder='static', template_folder='templates')

@bp.route('/')
def index():
    return "Index page"

@bp.route('/<infrastructure_type>')
def get_infrastructure(infrastructure_type):
    return infrastructure_type

@bp.route('/<region>')
def get_region(region):
    # return json as a dict corresponding to the region passed to the url.
    # we need to figure out how to map checkbox selections on the front
    # end bp to meaningful url params that we extract here.
    return region