from flask.wrappers import Request
from energy_maps_api.energy_maps_mongo_document import EnergyMapsMongoDocument
from flask import Blueprint, request
from flask.json import jsonify
from energy_maps_api.constants import URL_PREFIX
import energy_maps_api.errors.views as errors


bp = Blueprint('create_resource', __name__,
               url_prefix=URL_PREFIX)


# TODO: Add support for JWT authentication
@bp.route('/add_infrastructure', methods=['POST'])
def add_infrastructure():
    test = 0 # MDB operations to query db for existing record
    if test:
        return errors.conflict()
    else:
        if request.get_json() is not None:
            new_infrastructure = EnergyMapsMongoDocument() # perform MDB operations to add to db
            pass # do something in Mongo w/ the JSON data
            if new_infrastructure:
                return jsonify(new_infrastructure, message="Infrastructure added successfully"), 201
        else: 
            return errors.bad_request()

# The below Stack Overflow post gives example code for roughly how a user would interface w/
# the API programmatically:
# https://stackoverflow.com/questions/9746303/how-do-i-send-a-post-request-as-a-json/26876308#26876308