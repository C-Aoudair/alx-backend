#!/usr/bin/env python3
""" Contains FIFOCache class that inherites from BaseCaching.
"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ Implement caching system with fifo eviction policy.
    """
    def __init__(self):
        super().__init__()
        self.maxItems = BaseCaching.MAX_ITEMS

    def put(self, key, item):
        """ Adds item to self.cache_date dictionary"""
        if key and item:
            if len(self.cache_data) < self.maxItems:
                self.cache_data[key] = item
            else:
                firstKey = next(iter(self.cache_data))
                print(f"DISCARD: {firstKey}")
                self.cache_data.pop(firstKey)
                self.cache_data[key] = item

    def get(self, key):
        """Returns the value in self.cache_data linked to key."""
        return self.cache_data.get(key)
