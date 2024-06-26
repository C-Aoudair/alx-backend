#!/usr/bin/python3
""" Contains BasicCache Class that inherits from BaseCaching class.
"""

from BaseCaching import BaseCaching

class BasicCache(BaseCaching):
    """ a simple caching system"""
    def put(self, key, item):
        """assing a key item pair to the self.cache_data dictionary"""
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        """return the value in self.cache_data linked to key"""
        return self.cache_data.get(key)
