#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
try:
    import configparser
except ImportError:
    import configparser as configparser


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

config_file = configparser.ConfigParser()
config_file.read(os.path.join(
    BASE_DIR, 'static', 'config.ini'
))

MONGO = dict(
    local=True,
    user=config_file.get('user', 'username'),
    password=config_file.get('user', 'password'),
    domain=config_file.get('server', 'domain'),
    database=config_file.get('server', 'database'),
    port=int(config_file.get('server', 'port')),
)

URI = "mongodb://{}:{}@{}/{}?authMechanism=SCRAM-SHA-1".format(
    MONGO['user'], MONGO['password'], MONGO['domain'],
    MONGO['database'])
