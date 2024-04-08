#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
try:
    import simplejson as json
except ImportError:
    import json
from pymongo import MongoClient, GEOSPHERE
from energy_maps_api.constants import MONGO, URI


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

    @staticmethod
    def parse_url(url):
        url_list = url.strip('/').split('/')
        # TODO: This hardcoding is shit. It should be specified in the URI.
        key_list = ['primary', 'secondary', 'year', 'k']
        prop_dict = {}
        for i, x in enumerate(url_list):
            try:
                prop_dict[key_list[i]] = int(x)
            except ValueError:
                prop_dict[key_list[i]] = x
        return prop_dict

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

    def get_from_url(self, url):
        props = self.parse_url(url)
        return {
            'type': 'FeatureCollection',
            'features': list(self.get_from_props(props))
        }

    def get_from_props(self, props):
        if props['primary'] in ['electric_grid', 'railroads', 'pipelines']:
            pipeline = [{
                '$match': {
                    'properties.required.years.nominal': props['year'],
                    'properties.type.primary': props['primary'],
                    'properties.type.secondary': props['secondary'],
                    'geometry.type': 'LineString',
                }
            }, {
                '$project': {
                    '_id': 0,
                    'properties.original.class': 1,
                    'geometry.type': 1,
                    'geometry.coordinates': {
                        '$map': {
                            'input': '$geometry.coordinates',
                            'as': 'coords',
                            'in': {
                                '$map': {
                                    'input': '$$coords',
                                    'as': 'coord',
                                    'in': {
                                        '$round': ['$$coord', 4]
                                    }}}}}}}]
        elif props['primary'] in ['wells']:
            pipeline = [{
                '$match': {
                    'properties.required.years.nominal': props['year'],
                    'properties.type.primary': props['primary'],
                    'properties.type.secondary': props['secondary'],
                }
            }, {
                '$addFields': {
                    'lon': {
                        '$round': [
                            {'$arrayElemAt': ['$geometry.coordinates', 0]},
                            {'$floor': {'$sqrt': props['k']}}
                        ]
                    },
                    'lat': {
                        '$round': [
                            {'$arrayElemAt': ['$geometry.coordinates', 1]},
                            {'$floor': {'$sqrt': props['k']}}
                        ]
                    }
                }
            }, {
                '$addFields': {
                    'lonlat': {'$concat': [{'$toString': '$lon'},
                                           {'$toString': '$lat'}]},
                }
            }, {
                '$sort': {'lonlat': 1}
            }, {
                '$group': {
                    '_id': {'lonlat': '$lonlat'},
                    'zoom': {'$first': '$properties.original.zoom'},
                    'oilgas': {'$first': '$properties.original.oilgas'},
                    'class': {'$first': '$properties.original.class'},
                    'lon': {'$first': {'$round': [{
                        '$arrayElemAt': ['$geometry.coordinates', 0]}, 4]}},
                    'lat': {'$first': {'$round': [{
                        '$arrayElemAt': ['$geometry.coordinates', 1]}, 4]}},
                    'type': {'$first': '$geometry.type'},
                }
            }, {
                '$project': {
                    '_id': 0,
                    'geometry.type': '$type',
                    'geometry.coordinates': ['$lon', '$lat'],
                    'properties.original.zoom': '$zoom',
                    'properties.original.oilgas': '$oilgas',
                    'properties.original.class': '$class',
                }
            }]
        elif props['primary'] in ['power_plants']:
            pipeline = [{
                '$match': {
                    'properties.required.years.nominal': props['year'],
                    'properties.type.primary': props['primary'],
                    'properties.type.secondary': props['secondary'],
                }
            }, {
                '$project': {
                    '_id': 0,
                    'properties.original.SUMMER_CAP': 1,
                    'properties.original.total_cap': 1,
                    'geometry.type': 1,
                    'geometry.coordinates': {
                        '$map': {
                            'input': '$geometry.coordinates',
                            'as': 'coord',
                            'in': {
                                '$round': ['$$coord', 4]
                            }
                        }
                    }
                }
            }]
        elif props['primary'] in ['refineries']:
            pipeline = [{
                '$match': {
                    'properties.required.years.nominal': props['year'],
                    'properties.type.primary': props['primary'],
                    'properties.type.secondary': props['secondary'],
                }
            }, {
                '$project': {
                    '_id': 0,
                    'properties.original': 1,
                    'geometry.type': 1,
                    'geometry.coordinates': {
                        '$map': {
                            'input': '$geometry.coordinates',
                            'as': 'coord',
                            'in': {
                                '$round': ['$$coord', 4]
                            }}}}}]
        elif props['primary'] in ['mines']:
            pipeline = [{
                '$match': {
                    'properties.required.years.nominal': props['year'],
                    'properties.type.primary': props['primary'],
                    'properties.type.secondary': props['secondary'],
                }
            }, {
                '$project': {
                    '_id': 0,
                    'properties.original.tot_prod': 1,
                    'geometry.type': 1,
                    'geometry.coordinates': {
                        '$map': {
                            'input': '$geometry.coordinates',
                            'as': 'coord',
                            'in': {
                                '$round': ['$$coord', 4]
                            }}}}}]
        else:
            pipeline = [{
                '$match': {
                    'properties.required.years.nominal': props['year'],
                    'properties.type.primary': props['primary'],
                    'properties.type.secondary': props['secondary'],
                }
            }, {
                '$project': {
                    '_id': 0,
                    'geometry.type': 1,
                    'geometry.coordinates': {
                        '$map': {
                            'input': '$geometry.coordinates',
                            'as': 'coord',
                            'in': {
                                '$round': ['$$coord', 4]
                            }}}}}]
            proj = {'geometry': 1, '_id': 0}
        return self.db['infrastructure'].aggregate(pipeline)


if __name__ == '__main__':
    api = EnergyMapsAPI()
    api.load_geojson('input/coal.json')
    print(api.data)
    api.ingest(['total_cap'], 'power_plant', 'coal')
