"""
config.py
"""

import json

f = open('config.json')
conf = json.load(f)

class Config(object):
    def __init__(self):
        self._config = conf

    def get_property(self, property_name):
        if property_name not in self._config.keys():
            return None
        return self._config[property_name]