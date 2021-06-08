from flask import Flask
from energy_maps_api import funcs

app = Flask(__name__)

@app.route('/')
def index():
    return "Index page"

@app.route('/<infrastructure_type>')
def get_infrastructure(infrastructure_type):
    return infrastructure_type

@app.route('/<region>')
def get_region(region):
    return region

@app.route('/upload', methods=['POST'])
def upload():
    return funcs.upload_infrastructure_type()
