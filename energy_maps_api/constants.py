#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

cf = configparser.ConfigParser()
cf.read(os.path.join(
    BASE_DIR, 'static', 'config.ini'
))

MONGO = dict(
    local=True,
    user=cf.get('user', 'username'),
    password=cf.get('user', 'password'),
    domain=cf.get('server', 'domain'),
    database=cf.get('server', 'database'),
    port=int(cf.get('server', 'port')),
)

URI = "mongodb://{}:{}@{}/{}?authMechanism=SCRAM-SHA-1".format(
    MONGO['user'], MONGO['password'], MONGO['domain'],
    MONGO['database'])
