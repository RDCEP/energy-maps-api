from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Index page"

@app.route('/<infrastructure_type>')
def get_infrastructure(infrastructure_type):
    return infrastructure_type

@app.route('/<region>')
def get_region(region):
    # return json as a dict corresponding the region passed to the url
    # we need to figure out how to map checkbox selections on the front
    # end app to meaningful url params that we extract here
    return region

@app.route('/upload', methods=['POST'])
def upload():
    return 'Upload infrastructure type'
