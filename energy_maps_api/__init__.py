#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from energy_maps_api.create.views import bp as create_bp
from energy_maps_api.retrieve.views import bp as retrieve_bp
from energy_maps_api.update.views import bp as update_bp
from energy_maps_api.delete.views import bp as delete_bp

app = Flask(__name__)

app.register_blueprint(create_bp)
app.register_blueprint(retrieve_bp)
app.register_blueprint(update_bp)
app.register_blueprint(delete_bp)


@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def not_found(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(500)
def not_found(error):
    return render_template('errors/500.html'), 500
