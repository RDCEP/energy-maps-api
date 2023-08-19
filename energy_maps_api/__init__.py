#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from flask import Flask
# from flask import render_template
from energy_maps_api.create.views import bp as create_bp
from energy_maps_api.retrieve.views import bp as retrieve_bp
from energy_maps_api.update.views import bp as update_bp
from energy_maps_api.delete.views import bp as delete_bp
from energy_maps_api.errors.views import bp as errors_bp 
from energy_maps_api.app import app

# TODO: See if this conflicts with the same app definition in app.py
# app = Flask(__name__)

app.register_blueprint(create_bp)
app.register_blueprint(retrieve_bp)
app.register_blueprint(update_bp)
app.register_blueprint(delete_bp)
app.register_blueprint(errors_bp)
