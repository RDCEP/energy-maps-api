#!/usr/bin/env python
# -*- coding: utf-8 -*-
from energy_maps_api.energy_maps_schema import EnergyMapsSchema


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


