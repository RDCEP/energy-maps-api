# API will get called if we zoom in or out, when the user first goes to the site, when they turn on a new layer
# API won't get called when I reorder layers, when I turn off a layer
# Minimum retrieval is pass me a bounding box -- doesn't even have to be the right ones
try:
    import simplejson as json
except ImportError:
    import json
import gzip
from flask import Blueprint, jsonify, Response, request
from flask import make_response
from energy_maps_api.constants import URL_PREFIX
import energy_maps_api.errors.views as errors
from energy_maps_api.main import EnergyMapsAPI


bp = Blueprint('retrieve_resource', __name__,
               url_prefix=URL_PREFIX)
api = EnergyMapsAPI()


@bp.route('/')
def index():
    return "Index page"


@bp.route('<path:url>', methods=['GET'])
def get_infrastructure2(url):
    data = api.get_from_url(url)
    data = json.dumps(data).encode('utf8')
    # content = gzip.compress(json.dumps(data).encode('utf8'), 5)
    content = gzip.compress(data, 5)
    response = make_response(content)
    response.headers['Content-length'] = len(content)
    response.headers['Content-Encoding'] = 'gzip'
    # response = Response(json.dumps(data), mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# pass a bounding box, a filter for types of info (only coal power plants)
# can be more minimal than that for the first go around though
@bp.route('/<string:infrastructure_type>')
def get_infrastructure(infrastructure_type: str, bounding_box, methods=['GET']):
    print(2)
    result = 0 # MDB operations to retriever infrastructure_type 
               # from the db
    if result:
        return jsonify(result)
    else: 
        return errors.not_found()


@bp.route('/<region>')
def get_region(region):
    # return json as a dict corresponding to the region passed to the url.
    # we need to figure out how to map checkbox selections on the front
    # end bp to meaningful url params that we extract here.
    return region