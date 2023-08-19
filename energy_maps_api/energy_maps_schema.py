#!/usr/bin/env python
# -*- coding: utf-8 -*-
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


