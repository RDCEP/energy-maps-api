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


bp = Blueprint('retrieve_deck_resource', __name__,
               url_prefix='{}/deck/'.format(URL_PREFIX))
api = EnergyMapsAPI()


@bp.route('<path:url>', methods=['GET'])
def get_deck_infrastructure2(url):
    data = api.get_deck_from_url(url)
    data = json.dumps(data).encode('utf8')
    content = gzip.compress(data, 5)
    response = make_response(content)
    response.headers['Content-length'] = len(content)
    response.headers['Content-Encoding'] = 'gzip'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
