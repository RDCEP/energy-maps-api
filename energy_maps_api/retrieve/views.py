# API will get called if we zoom in or out, when the user first goes to the site, when they turn on a new layer
# API won't get called when I reorder layers, when I turn off a layer
# Minimum retrieval is pass me a bounding box -- doesn't even have to be the right ones
try:
    import simplejson as json
except ImportError:
    import json
from flask import Blueprint, jsonify, Response, request
from energy_maps_api.constants import URL_PREFIX
import energy_maps_api.errors.views as errors
from energy_maps_api.main import EnergyMapsAPI


bp = Blueprint('retrieve_resource', __name__,
               url_prefix=URL_PREFIX)
api = EnergyMapsAPI()


@bp.route('/')
def index():
    return "Index page"


# @bp.route('/mines/coal', methods=['GET'])
# def get_coal_mines(url):
#     props = {
#         'properties.type.primary': 'mines',
#         'properties.type.secondary': 'coal',
#         'properties.required.years.nominal': None,
#     }
#     data = api.get_from_props(url)
#     response = Response(json.dumps(data), mimetype='application/json')
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     return response


@bp.route('<path:url>', methods=['GET'])
def get_infrastructure2(url):
    data = api.get_from_url(url)
    response = Response(json.dumps(data), mimetype='application/json')
    # response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:3000'
    return response


# Example of getting url params from the client
# https://github.com/njmattes/goodfornothing/blob/master/goodfornothing/no1/views.py
# @mod.route('/init/<int:width>/<int:height>')
# def init(width, height):
#     session['width'] = width
#     session['height'] = height
#     session['area'] = width * height
#     arr = np.arange(session['area'])
#     np.random.shuffle(arr)
#     init_collection(session.sid)
#     write_idxs(arr, session.sid)
#     return Response(
#         json.dumps({'success': True}),
#         200,
#         {'ContentType': 'application/json'}
#     )

# Relevant client side example, put something like this in the front end app
# function pxls(t) {
#     /**
#      * If we have run through all pixels, set t back to 0, begin running
#      * the wipe() function, and return.
#      */
#     if (t >= width * height) {
#       t = 0;
#       wipe(t, width * height);
#       return;
#     }
#     d3.json(`/no1/get_${mode}/${t},${number}/${threshold}/${network}`, {
#       headers: {
#         'Content-type': 'application/json; charset=UTF-8'
#       }}).then(json => {
#         for (let i = 0; i < json['pxls'].length; ++i) {
#           fill_pxl(
#             json.pxls[i].color,
#             json.pxls[i].xy
#           );
#         }
#       });
#     t += number;
#     setTimeout(pxls.bind({}, t), timer);
#   }

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