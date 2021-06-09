#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from energy_maps_api.create.views import bp as create_bp
from energy_maps_api.retrieve.views import bp as retrieve_bp
from energy_maps_api.update.views import bp as update_bp
from energy_maps_api.delete.views import bp as delete_bp

app = Flask(__name__)

app.register_blueprint(create_bp)
app.register_blueprint(retrieve_bp)
app.register_blueprint(update_bp)
app.register_blueprint(delete_bp)