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
        collection = url_list[0]
        # TODO: This hardcoding is shit. It should be specified in the URI.
        key_list = ['year', 'k']
        prop_dict = {}
        for i, x in enumerate(url_list[1:]):
            try:
                prop_dict[key_list[i]] = int(x)
            except ValueError:
                prop_dict[key_list[i]] = x
        return collection, prop_dict

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
        collection, props = self.parse_url(url)
        return {
            'type': 'FeatureCollection',
            'features': list(self.get_from_props(props, collection))
        }

    def get_from_props(self, props, collection):
        match = {
            'properties.required.years.nominal': props['year'],
        }
        if collection in [
            'electric_grid_100_300_kV_AC', 'electric_grid_345_735_kV_AC',
            'electric_grid_under_100', 'railroads', 'electric_grid_dc',
            'pipelines_gas', 'pipelines_oil', 'pipelines_petroleum_product'
        ]:
            pipeline = [{
                '$match': {
                    'properties.required.years.nominal': props['year'],
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
            # proj = {'geometry': 1, 'properties.original.class': 1, '_id': 0}
        elif collection in [
            'wells_oil', 'wells_gas'
        ]:
            pipeline = [{
                '$match': {
                    # 'properties.original.zoom': props['k'],
                    'properties.required.years.nominal': props['year'],
                }
            }, {
                '$project': {
                    '_id': 0,
                    'properties.original.zoom': 1,
                    'properties.original.oilgas': 1,
                    'properties.original.class': 1,
                    'geometry.type': 1,
                    'geometry.coordinates': {
                        '$map': {
                            'input': '$geometry.coordinates',
                            'as': 'coord',
                            'in': {
                                '$round': ['$$coord', 4]
                            }}}}}]
        elif collection in [
            'power_plants_coal', 'power_plants_geothermal',
            'power_plants_hydroelectric', 'power_plants_natural_gas',
            'power_plants_nuclear', 'power_plants_petroleum',
            'power_plants_solar', 'power_plants_wind'
        ]:
            pipeline = [{
                '$match': {
                    'properties.required.years.nominal': props['year'],
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
                            }}}}}]
            # proj = {'geometry': 1, 'properties.original.SUMMER_CAP': 1,
            #         'properties.original.total_cap': 1, '_id': 0}
        elif collection in ['refineries_petroleum']:
            pipeline = [{
                '$match': {
                    'properties.required.years.nominal': props['year'],
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
            # proj = {'geometry': 1, 'properties.original': 1, '_id': 0}
        elif collection in ['mines_coal']:
            pipeline = [{
                '$match': {
                    'properties.required.years.nominal': props['year'],
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
            # proj = {'geometry': 1, 'properties.original.tot_prod': 1, '_id': 0}
        else:
            pipeline = [{
                '$match': {
                    'properties.required.years.nominal': props['year'],
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
        return self.db[collection].aggregate(pipeline)
        # return self.db[collection].find(props, projection=proj)


if __name__ == '__main__':
    api = EnergyMapsAPI()
    api.load_geojson('input/coal.json')
    print(api.data)
    api.ingest(['total_cap'], 'power_plant', 'coal')
