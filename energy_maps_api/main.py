#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
try:
    import simplejson as json
except ImportError:
    import json
from pymongo import MongoClient, GEOSPHERE
from energy_maps_api.constants import MONGO, URI


class EnergyMapsSchema(object):
    def __init__(self, x, y, properties):
        self.x = x
        self.y = y
        self.properties = properties

    @property
    def __geo_interface__(self):
        return dict()

    @property
    def as_dict(self):
        return self.__geo_interface__


class EnergyMapsMongoDocument(EnergyMapsSchema):
    def __init__(self, *args, **kwargs):
        """Schema for storing Energy Maps objects in Mongo.
        """
        super(EnergyMapsMongoDocument, self).__init__(*args, **kwargs)

    @property
    def __geo_interface__(self):
        """Define centroid (x, y) as a GeoJSON point.

        :return: GeoJSON object representing data point
        :rtype: dict
        """

        document = {
            'geometry': {'type': 'Point',
                         'coordinates': [self.x, self.y]},
            'properties': self.properties}
        return document


class EnergyMapsAPI(object):
    def __init__(self):
        self._json = None
        self._db = None
        self._data = None

    @property
    def json(self):
        """Temporary store for JSON data when a JSON file is ingested.
        The JSON is processed and held in the self.data property before
        ingestion.

        :return: A dictionary representing the JSON
        :rtype: dict
        """
        return self._json

    @property
    def db(self):
        """Connection to the Mongo db based on credentials found in the
        `static/config.ini` file.

        :return: An instance of a MongoClient connection
        :rtype: MongoClient
        """
        if self._db is None:
            client = MongoClient(URI) if not MONGO['local'] \
                else MongoClient('localhost', MONGO['port'])
            self._db = client[MONGO['database']]
        return self._db

    @property
    def data(self):
        """Temporary storage for data to be ingested.

        :return: Ingestable data
        :rtype: list
        """
        return self._data

    def load_geojson(self, path):
        """Load a GeoJSON document and stare its features for ingesting.

        :param path: Path to the GeoJSON file
        :return: Success
        :rtype: bool
        """
        _json = {}
        try:
            with open(path) as f:
                _json = json.loads(f.read())
        except IOError:
            print('FIle not found or not readable as JSON.')
            return False
        self._data = _json['features']
        return True

    def create_index(self):
        self.db.create_index([('geometry', GEOSPHERE)])

    def ingest(self, props_filter, primary, secondary):
        if self.data is None:
            raise TypeError('EnergyMapsAPI.data is None. '
                            'Have you loaded a data file?')
        docs = [
            dict(geometry=d['geometry'],
                 properties={k: v for k, v in
                             [['primary', primary]] +
                             [['secondary', secondary]] +
                             [[l, d['properties'][l]]
                              for l in props_filter]})
            for d in self.data]
        self.db['energy_shit'].insert_many(docs)
        print('{} documents ingested.'.format(len(docs)))
        return True


if __name__ == '__main__':
    api = EnergyMapsAPI()
    api.load_geojson('input/coal.json')
    print(api.data)
    api.ingest(['total_cap'], 'power_plant', 'coal')
