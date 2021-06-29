from energy_maps_api.main import EnergyMapsMongoDocument
from flask import Blueprint
from flask.json import jsonify
from energy_maps_api.constants import URL_PREFIX
import energy_maps_api.errors.views as errors


bp = Blueprint('create', __name__,
               url_prefix=URL_PREFIX)


# TODO: Add support for JWT authentication
@bp.route('/add_infrastructure/<string:file>', methods=['POST'])
def add_infrastructure(file: str):
    # read file from user, determine how best to do this
    # do we want to create a login system and a form for submitting?
    file = jsonify(file)
    test = 0 # MDB operations to query db for existing record
    if test:
        return errors.conflict()
    else:
        new_infrastructure = EnergyMapsMongoDocument() # MDB operations to add to db
    if new_infrastructure:
        return jsonify(new_infrastructure, message="Infrastructure added successfully"), 201
    else:
        return errors.not_found()#, jsonify(message="Please try to upload again.")